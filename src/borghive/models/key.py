from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from borghive.models.base import BaseModel
from borghive.lib.validators import ssh_public_key_validator
from borghive.lib import rules


class SSHPublicKey(BaseModel):

    name        = models.CharField(max_length=256)
    public_key  = models.TextField(max_length=2048, validators=[RegexValidator(regex=settings.BORGHIVE['SSH_PUBLIC_KEY_REGEX'], message="SSH Public Key should match format: ssh-xxx AAAA... comment"), ssh_public_key_validator])
    created     = models.DateTimeField(auto_now_add=True)
    owner       = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return 'SSHPublicKey: {}'.format(self.name)
