
from borghive.forms.base import BaseForm
from borghive.models import SSHPublicKey


class SSHPublicKeyForm(BaseForm):
    """
    form to create an ssh public key
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['public_key'].widget.attrs['placeholder'] = 'ssh-rsa AAAA... comment'

    class Meta:
        model = SSHPublicKey
        fields = ('public_key', 'name', 'group',)
