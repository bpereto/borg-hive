from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

from borghive.models.base import BaseModel


class SSHPublicKey(BaseModel):

    name        = models.CharField(max_length=256)
    public_key  = models.TextField(max_length=2048, validators=[RegexValidator(regex=settings.BORGHIVE['SSH_PUBLIC_KEY_REGEX'], message="SSH Public Key should match format: ssh-xxx AAAA... comment")])
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'SSHPublicKey: {}'.format(self.name)
