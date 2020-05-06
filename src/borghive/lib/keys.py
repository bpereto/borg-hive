import sshpubkeys
import os
import logging

LOGGER = logging.getLogger(__name__)

def get_ssh_host_key_infos():
    '''
    get fingerprints of ssh host keys
    '''
    KEY_TYPES = ['rsa', 'ecdsa', 'ed25519']

    data = {}
    for key_type in KEY_TYPES:
        file = os.path.join('/config', 'ssh_host_{}_key.pub'.format(key_type))
        if os.path.isfile(file):
            LOGGER.debug('found %', file)
            with open(file) as f:
                key = sshpubkeys.SSHKey(f.read())
                key.parse()
            data[key_type] = key.hash_sha256()
    LOGGER.debug(data)
    return data
