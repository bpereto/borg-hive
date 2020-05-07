
from borghive.forms import BaseForm
from borghive.models import SSHPublicKey


class SSHPublicKeyCreateForm(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['public_key'].widget.attrs['placeholder'] = 'ssh-rsa AAAA... comment'

    class Meta:
        model = SSHPublicKey
        fields = ('public_key', 'name',)


class SSHPublicKeyUpdateForm(BaseForm):

    class Meta:
        model = SSHPublicKey
        fields = ('public_key', 'name',)
