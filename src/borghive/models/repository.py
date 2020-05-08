import datetime
import glob
import logging
import os
import random
import subprocess

from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware

import borghive.exceptions
from borghive.models.base import BaseModel

from .key import SSHPublicKey

LOGGER = logging.getLogger(__name__)


class RepositoryUser(BaseModel):
    """
    repository user model

    represents a uniq user related to one repository
    """
    name = models.CharField(max_length=8, unique=True)

    def __str__(self):
        """representation"""
        return 'RepositoryUser: {}'.format(self.name)

    def get_passwd_line(self):
        """compile passwd line"""

        PASSWD_LINE_PATTERN = '{}:x:{}:{}:Borghive Repository User:{}:/bin/bash\n'

        homedir = os.path.join(settings.BORGHIVE['REPO_PATH'], self.name)
        LOGGER.debug('get_passwd_line: homedir: %s', homedir)

        return PASSWD_LINE_PATTERN.format(self.name, self.id, self.id, homedir)

    def get_shadow_line(self):
        """compile shadow line"""

        SHADOW_LINE_PATTERN = '{}:*:18384:0:99999:7:::\n'

        shadow_line = SHADOW_LINE_PATTERN.format(self.name)
        LOGGER.debug('get_shadow_line: %s', shadow_line)

        return shadow_line


class Repository(BaseModel):
    """
    repository model

    core of borghive and does a lot of things.

    * repo status
    * alert check/alerting
    * refresh statistics
    """

    name = models.CharField(max_length=256, validators=[RegexValidator(regex=r'^[\w\-\.]+$')])
    ssh_keys = models.ManyToManyField(SSHPublicKey)
    #    append_only_keys = models.ManyToManyField(SSHPublicKey)
    repo_user = models.OneToOneField(RepositoryUser, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    last_updated = models.DateTimeField(null=True, blank=True)
    last_access = models.DateTimeField(null=True, blank=True)

    alert_after_days = models.IntegerField(null=True, blank=True)  # days

    def __str__(self):
        """representation"""
        return 'Repository: {}'.format(self.name)

    def get_repo_path(self):
        '''
        path to repo on fs

        /repos/<repo user>/<repo name>
        '''
        return os.path.join(settings.BORGHIVE['REPO_PATH'], self.repo_user.name, self.name)

    def is_created(self):
        '''
        check if repository is already setup and created
        '''
        config = os.path.join(self.get_repo_path(), 'config')
        if os.path.isdir(self.get_repo_path()) and os.path.isfile(config):
            return True
        return False

    def is_encrypted(self):
        '''
        check if repository is encrypted
        '''
        if self.is_created():
            config = os.path.join(self.get_repo_path(), 'config')
            with open(config, 'r') as f:
                return'key =' in f.read()
        return False

    def get_last_access_by_fs(self):
        '''
        get last repository access
        estimated on last change of nonce file in repository
        '''
        if self.is_created():
            last_access = os.path.getmtime(self.get_repo_path())
            return make_aware(datetime.datetime.fromtimestamp(last_access))
        return None

    def get_last_updated_by_fs(self):
        '''
        get last repository update
        as every thing is encrypted, the modification is estimated on
        the last change of the index.x file
        '''
        if self.is_created():
            index_file = glob.glob(os.path.join(
                self.get_repo_path(), 'index.*'))
            if len(index_file) != 1:
                raise Exception('Too many index files found')
            last_updated = os.path.getmtime(index_file[0])
            return make_aware(datetime.datetime.fromtimestamp(last_updated))
        return None

    def get_repo_size(self):
        '''
        get repository size in megabytes
        estimated on how much filespace is occupied
        heavy operation on fs!
        '''
        if self.is_created():
            data_path = os.path.join(self.get_repo_path(), 'data')
            return subprocess.check_output(['du', '-sm', data_path]).split()[0].decode('utf-8')
        return None

    def get_last_repository_statistic(self):
        """get last saved repository statistic for this repo"""
        return self.repositorystatistic_set.last()

    def refresh(self):
        '''
        persistens recent repo statistic
        '''

        if self.is_created():
            LOGGER.info('refresh: %s', self.name)

            # update acess infos
            self.last_updated = self.get_last_updated_by_fs()
            self.last_access = self.get_last_access_by_fs()
            self.save()

            # create statistic
            statistic = RepositoryStatistic(repo_size=self.get_repo_size())
            statistic.repo = self
            statistic.save()
        else:
            raise borghive.exceptions.RepositoryNotCreated()

    def should_alert(self):
        '''
        check if alert should be fired

        firing : update time is older than alert time
        alert  : should alert, considered alert expiration and interval
        '''
        # pylint: disable=no-member

        alert = False
        firing = False

        if not self.last_updated or not self.alert_after_days:
            return firing, alert

        # calculate point in time to fire alert
        alert_time = self.last_updated + \
            datetime.timedelta(days=self.alert_after_days)

        if alert_time <= timezone.now():
            LOGGER.debug('Alert Time hit: last update %s is older than %s',
                         self.last_updated, alert_time)
            firing = True
            alert = True

            #
            # check alert interval
            #
            last_alert = self.repositoryevent_set.filter(
                event_type=RepositoryEvent.ALERT, created__gte=self.last_updated).last()

            if last_alert:
                next_alert_interval = last_alert.created + \
                    datetime.timedelta(
                        hours=self.owner.alertpreference.alert_interval)
                if timezone.now() < next_alert_interval:
                    LOGGER.debug('Last alert was not too long ago: %s, alert interval is set to: %s',
                                 last_alert.created, self.owner.alertpreference.alert_interval)
                    alert = False

                #
                # check alert expiration
                #
                alert_expired_time = self.last_updated + \
                    datetime.timedelta(
                        days=self.owner.alertpreference.alert_expiration)
                if alert_expired_time < timezone.now():
                    LOGGER.debug('Alert expired: last alert %s is older than set alert expiration: %s',
                                 last_alert, self.owner.alertpreference.alert_expiration)
                    alert = False
        return firing, alert

    def alert(self):
        '''
        alert owner for missing backups
        notify via configured notifications
        '''
        import borghive.tasks.alert  # pylint: disable=import-outside-toplevel

        LOGGER.info('%s: alerting', self)
        delta = timezone.now()-self.last_updated
        alert = RepositoryEvent(event_type=RepositoryEvent.ALERT, message='Last backup of {} is older than {} days'.format(
            self.name, delta.days), repo=self)
        alert.save()

        borghive.tasks.alert.fire_alert.delay(
            repo_id=self.id, alert_id=alert.id)

    class Meta():
        verbose_name_plural = 'Repositories'

        # user and reponame should be unique
        unique_together = ['name', 'repo_user']


class RepositoryStatistic(BaseModel):
    """
    repository statistic
    """
    repo_size = models.IntegerField()  # mega bytes
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)

    def __str__(self):
        """representation"""
        return 'RepositoryStatistic: {} for {}'.format(self.created, self.repo)


class RepositoryEvent(BaseModel):
    """
    represents an event happened in relation to a repository
    """

    WATCHER = 'watcher'
    ALERT = 'alert'

    EVENT_TYPES = [
        (WATCHER, 'watcher'),
        (ALERT, 'alert'),
    ]

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    message = models.TextField(max_length=200)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)

    def __str__(self):
        return 'RepositoryEvent: {}: {}'.format(self.event_type, self.message)
