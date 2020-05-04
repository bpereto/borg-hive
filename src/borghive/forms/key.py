from django import forms

from borghive.models import SSHPublicKey


class SSHPublicKeyCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['public_key'].widget.attrs['placeholder'] = 'ssh-rsa AAAA... comment'

    class Meta:
        model = SSHPublicKey
        fields = ('public_key','name',)


class SSHPublicKeyUpdateForm(forms.ModelForm):

    class Meta:
        model = SSHPublicKey
        fields = ('public_key','name',)
