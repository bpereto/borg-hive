import logging
import os
from django.conf import settings

import sshpubkeys

LOGGER = logging.getLogger(__name__)


def get_ssh_host_key_infos():
    '''
    get fingerprints of ssh host keys
    '''
    KEY_TYPES = ['rsa', 'ecdsa', 'ed25519']

    data = {}
    for key_type in KEY_TYPES:
        file = os.path.join(settings.BORGHIVE['CONFIG_PATH'], f'ssh_host_{key_type}_key.pub')
        if os.path.isfile(file):
            LOGGER.debug('found %s', file)
            with open(file) as f:  # pylint: disable=W1514
                key = sshpubkeys.SSHKey(f.read())
                key.parse()
            data[key_type] = key.hash_sha256()
    LOGGER.debug(data)
    return data
