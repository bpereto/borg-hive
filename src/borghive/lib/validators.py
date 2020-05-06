import sshpubkeys
import logging

from django.core.exceptions import ValidationError

LOGGER = logging.getLogger(__name__)


def ssh_public_key_validator(public_key):
    '''
    validate public key string
    '''
    key = sshpubkeys.SSHKey(public_key)
    try:
        key.parse()
    except sshpubkeys.InvalidKeyError as exc:
        LOGGER.exception(exc)
        raise ValidationError('Malformed SSH Public Key')
