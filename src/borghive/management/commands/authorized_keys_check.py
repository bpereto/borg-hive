import logging

from django.core.management.base import BaseCommand

from borghive.models import RepositoryUser

LOGGER = logging.getLogger(__name__)

KEY_CMD_PREFIX = 'command="borg serve '
KEY_CMD_POSTFIX = '",restrict '


class Command(BaseCommand):
    '''
    django management command to present the ssh-keys from the database
    as authorized_keys format
    '''
    help = 'Get Authorized Keys from Database'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str)

    def handle(self, *args, **options):

        user = RepositoryUser.objects.get(name=options['user'])

        # add restrict to repository
        for key in user.repository.ssh_keys.all():
            LOGGER.debug(key)
            command_options = []

            # restrict path
            command_options.append('--restrict-to-repository {}'.format(user.repository.get_repo_path()))

            authorized_keys_line = KEY_CMD_PREFIX + \
                ' '.join(command_options) + KEY_CMD_POSTFIX + key.public_key
            LOGGER.debug(authorized_keys_line)

            print(authorized_keys_line)

        # add append only mode
        for key in user.repository.append_only_keys.all():
            LOGGER.debug(key)
            command_options = []

            command_options.append('--append-only')

            # restrict path
            command_options.append('--restrict-to-repository {}'.format(user.repository.get_repo_path()))

            authorized_keys_line = KEY_CMD_PREFIX + \
                ' '.join(command_options) + KEY_CMD_POSTFIX + key.public_key
            LOGGER.debug(authorized_keys_line)

            print(authorized_keys_line)
    