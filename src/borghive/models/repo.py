import os
import glob
import random
import string
import subprocess

from datetime import datetime
import logging

from django.db import models
from django.conf import settings
from django.utils.timezone import make_aware
from django.contrib.auth.models import User

from borghive.exceptions import RepositoryNotCreated
from borghive.models.base import BaseModel

from .key import SSHPublicKey


LOGGER = logging.getLogger(__name__)


def generate_userid(uid_length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(uid_length))


class RepositoryUser(BaseModel):
    name = models.CharField(max_length=8, unique=True, default=generate_userid(8))

    def __str__(self):
        return 'RepositoryUser: {}'.format(self.name)

    def get_passwd_line(self):
        PASSWD_LINE_PATTERN = '{}:x:{}:{}:Borghive Repository User:{}:/bin/bash\n'
        homedir = os.path.join(settings.BORGHIVE['REPO_PATH'], self.name)
        LOGGER.debug('get_passwd_line: homedir: %s', homedir)
        return PASSWD_LINE_PATTERN.format(self.name, self.id, self.id, homedir)

    def get_shadow_line(self):
        SHADOW_LINE_PATTERN = '{}:*:18384:0:99999:7:::\n'
        shadow_line = SHADOW_LINE_PATTERN.format(self.name)
        LOGGER.debug('get_shadow_line: %s', shadow_line)
        return shadow_line


class Repository(BaseModel):

    name        = models.CharField(max_length=30, unique=True)
    ssh_keys    = models.ManyToManyField(SSHPublicKey)
    #    append_only_keys = models.ManyToManyField(SSHPublicKey)
    repo_user   = models.OneToOneField(RepositoryUser, on_delete=models.CASCADE)
    owner       = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
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
        if is_created:
            return False
        return False

    def get_last_access(self):
        '''
        get last repository access
        estimated on last change of nonce file in repository
        '''
        if self.is_created():
            last_access = os.path.getmtime(self.get_repo_path())
            return make_aware(datetime.fromtimestamp(last_access))
        return None

    def get_last_updated(self):
        '''
        get last repository update
        as every thing is encrypted, the modification is estimated on
        the last change of the index.x file
        '''
        if self.is_created():
            index_file = glob.glob(os.path.join(self.get_repo_path(), 'index.*'))
            if len(index_file) != 1:
                raise Exception('Too many index files found')
            last_updated = os.path.getmtime(index_file[0])
            return make_aware(datetime.fromtimestamp(last_updated))
        return None

    def get_repo_size(self):
        '''
        get repository size in megabytes
        estimated on how much filespace is occupied
        heavy operation on fs!
        '''
        if self.is_created():
            data_path = os.path.join(self.get_repo_path(), 'data')
            return subprocess.check_output(['du','-sm', data_path]).split()[0].decode('utf-8')
        return None

    def get_last_repository_statistic(self):
        return self.repositorystatistic_set.last()

    def refresh(self):

        if self.is_created():
            stats = {
                'repo_size': self.get_repo_size(),
                'last_update': self.get_last_updated(),
                'last_access': self.get_last_access()
            }
            statistic = RepositoryStatistic(**stats)
            statistic.repo = self
            statistic.save()

    class Meta():
        verbose_name_plural = 'Repositories'


class RepositoryStatistic(BaseModel):
    repo_size = models.IntegerField()  # mega bytes
    last_update = models.DateTimeField()
    last_access = models.DateTimeField()
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)

    def __str__(self):
        return 'RepositoryStatistic: {} for {}'.format(self.created, self.repo)
