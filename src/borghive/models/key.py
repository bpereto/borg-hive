import logging

import sshpubkeys
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.db import models

from borghive.lib.validators import ssh_public_key_validator
from borghive.models.base import BaseModel
from borghive.managers import OwnerOrGroupManager

LOGGER = logging.getLogger(__name__)


class SSHPublicKey(BaseModel):
    """
    represents a ssh public key

    initially, the public key is provided by the user and checked against the
    regex pattern SSH_PUBLIC_KEY_REGEX.
    if valid, the key is parsed by "sshpublickeys" library and the different
    fields (comment, bits, type etc.) of this model are updated.
    """

    name = models.CharField(max_length=256)
    public_key = models.TextField(max_length=2048, validators=[RegexValidator(
        regex=settings.BORGHIVE['SSH_PUBLIC_KEY_REGEX'], message="SSH Public Key should match format: ssh-xxx AAAA... comment"), ssh_public_key_validator])

    type = models.CharField(max_length=50)
    bits = models.IntegerField()
    fingerprint = models.CharField(max_length=256)
    comment = models.CharField(max_length=256, null=True)

    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    group = models.ManyToManyField(Group, blank=True)

    objects = OwnerOrGroupManager()

    def __str__(self):
        """representation"""
        return 'SSHPublicKey: {}'.format(self.name)

    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        """override save to parse public key"""
        self._parse_public_key()
        super().save(*args, **kwargs)

    def _parse_public_key(self):
        """parse publickey and update fiels"""
        key = sshpubkeys.SSHKey(self.public_key)
        key.parse()

        self.type = key.key_type.decode('utf-8').replace('ssh-', '')
        self.bits = key.bits
        self.fingerprint = key.hash_sha256()
        self.comment = key.comment

        LOGGER.debug(self.__dict__)
