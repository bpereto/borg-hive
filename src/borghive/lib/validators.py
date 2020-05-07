import logging

import sshpubkeys
from django.core.exceptions import ValidationError

LOGGER = logging.getLogger(__name__)


def ssh_public_key_validator(public_key):
    '''
    validate public key string
    '''
    try:
        key = sshpubkeys.SSHKey(public_key)
        key.parse()
    except (sshpubkeys.InvalidKeyError, sshpubkeys.exceptions.MalformedDataError, UnicodeEncodeError) as exc:
        LOGGER.exception(exc)
        raise ValidationError('Malformed SSH Public Key')
