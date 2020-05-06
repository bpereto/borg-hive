import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from borghive.models import RepositoryUser, SSHPublicKey

LOGGER = logging.getLogger(__name__)

KEY_CMD_PREFIX = 'command="borg serve '
KEY_CMD_POSTFIX = '",restrict '


class Command(BaseCommand):
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

            authorized_keys_line = KEY_CMD_PREFIX + ' '.join(command_options) + KEY_CMD_POSTFIX + key.public_key
            LOGGER.debug(authorized_keys_line)
            print(authorized_keys_line)
