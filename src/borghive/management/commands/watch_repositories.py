import logging
import os

import inotify.adapters
from django import db
from django.core.management.base import BaseCommand

# used for singal activation
import borghive.signals  # pylint: disable=unused-import
from borghive.models.repo import Repository, RepositoryEvent

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Command(BaseCommand):
    '''
    django management command to watch borg repository changes on fs with inotify
    '''
    help = 'Watch Repositories for changes'

    def add_arguments(self, parser):
        """arguments parser"""
        parser.add_argument('--repo-path', type=str)

    def get_repo_by_path(self, path):  # pylint: disable=no-self-use
        """distill repo name from inotify path"""
        repo_name = path.split('/')[-1]
        repo_user = path.split('/')[-2]
        db.close_old_connections()
        repo = Repository.objects.get(
            name=repo_name, repo_user__name=repo_user)
        LOGGER.debug('get_repo_by_path: %s', repo)
        return repo

    def handle(self, *args, **options):
        '''
        install inotify watcher for repository directory
        this can generate a large amount of events when there are many or large repositories.
        '''

        if not os.path.isdir(options['repo_path']):
            raise Exception(
                'Repo path: {} not found'.format(options['repo_path']))

        i = inotify.adapters.InotifyTree(options['repo_path'])

        for event in i.event_gen(yield_nones=False):

            try:
                (_, type_names, path, filename) = event

                LOGGER.debug("PATH=[%s] FILENAME=[%s] EVENT_TYPES=%s", path, filename, type_names)

                # Event handling
                if filename == 'lock.exclusive':
                    LOGGER.info('lock detected: repo access')

                    repo = self.get_repo_by_path(path)

                    # repo open
                    if 'IN_CREATE' in type_names:
                        LOGGER.info('lock created: repo open: %s', repo)

                        log_event = RepositoryEvent(
                            event_type='watcher', message='Repository open', repo=repo)
                        log_event.save()

                    # repo close
                    if 'IN_DELETE' in type_names:
                        LOGGER.info('lock deleted: repo close: %s', repo)
                        log_event = RepositoryEvent(
                            event_type='watcher', message='Repository closed', repo=repo)
                        log_event.save()

                # repo created
                if filename == 'README' and 'IN_CREATE' in type_names:
                    repo = self.get_repo_by_path(path)
                    LOGGER.info(
                        'repo created: readme created - indicates repo creation: %s', repo)

                    log_event = RepositoryEvent(
                        event_type='watcher', message='Repository created', repo=repo)
                    log_event.save()

                # repo updated: there is no clear indicator what is done
                if filename.startswith('index.') and 'IN_MOVED_TO' in type_names:
                    repo = self.get_repo_by_path(path)
                    LOGGER.info('repo updated: %s', repo)

                    log_event = RepositoryEvent(
                        event_type='watcher', message='Repository updated', repo=repo)
                    log_event.save()

                if 'IN_DELETE_SELF' in type_names:
                    is_repo_path = len(path.replace(
                        options['repo_path'], '').split('/')) == 2
                    if is_repo_path:
                        repo = self.get_repo_by_path(path)
                        LOGGER.info('repo deleted: %s', repo)

                        log_event = RepositoryEvent(
                            event_type='watcher', message='Repository deleted', repo=repo)
                        log_event.save()

            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.exception(exc)
