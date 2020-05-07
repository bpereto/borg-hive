import logging

import sshpubkeys
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from borghive.lib.validators import ssh_public_key_validator
from borghive.models.base import BaseModel

LOGGER = logging.getLogger(__name__)


class SSHPublicKey(BaseModel):

    name = models.CharField(max_length=256)
    public_key = models.TextField(max_length=2048, validators=[RegexValidator(
        regex=settings.BORGHIVE['SSH_PUBLIC_KEY_REGEX'], message="SSH Public Key should match format: ssh-xxx AAAA... comment"), ssh_public_key_validator])

    type = models.CharField(max_length=15)
    bits = models.IntegerField()
    fingerprint = models.CharField(max_length=256)
    comment = models.CharField(max_length=256)

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return 'SSHPublicKey: {}'.format(self.name)

    def save(self, *args, **kwargs):
        self._parse_public_key()
        super().save(*args, **kwargs)

    def _parse_public_key(self):
        '''
        parse publickey and update fiels
        '''
        key = sshpubkeys.SSHKey(self.public_key)
        key.parse()

        self.type = key.key_type.decode('utf-8').replace('ssh-', '')
        self.bits = key.bits
        self.fingerprint = key.hash_sha256()
        self.comment = key.comment

        LOGGER.debug(self.__dict__)
