
import logging
import os
import sys

from django import db
from django.core.management.base import BaseCommand
from django.conf import settings

# used for singal activation
import borghive.signals  # pylint: disable=unused-import
from borghive.models.repository import Repository, RepositoryEvent

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARNING)

# pylint: disable=too-many-nested-blocks


class Command(BaseCommand):
    '''
    django management command to log a borgbackup event
    '''
    help = 'Log Borgbackup event'

    events = {
        'get': 'repository open',
        'commit': 'created archive',
        'rollback': 'rollback',
        'save_key': 'saved key (created)',
        'list': 'repository list'
    }

    def add_arguments(self, parser):
        """arguments parser"""
        parser.add_argument('--event', type=str)
        parser.add_argument('--repo-path', type=str)

    def get_repo_by_path(self, path):  # pylint: disable=no-self-use
        """distill repo name from repo path"""
        repo_name = path.split('/')[-1]
        repo_user = path.split('/')[-2]
        db.close_old_connections()
        repo = Repository.objects.get(
            name=repo_name, repo_user__name=repo_user)
        LOGGER.debug('get_repo_by_path: %s', repo)
        return repo

    def handle(self, *args, **options):
        ''' '''
        # handle log event
        repo_path = options['repo_path']
        event = options['event']
        LOGGER.debug('repo_path=%s event=%s', repo_path, event)

        if self.events.get(event):
            repo = self.get_repo_by_path(repo_path)
            LOGGER.info('create repo event: %s for %s', event, repo)
            log_event = RepositoryEvent(event_type='borg', message=self.events.get(event), repo=repo)
            log_event.save()
