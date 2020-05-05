from django import forms

from borghive.models import Repository, SSHPublicKey
from borghive.forms import BaseForm


class RepositoryCreateForm(BaseForm):


    class Meta:
        model = Repository
        fields = '__all__'
        exclude = ('repo_user','owner')


class RepositoryUpdateForm(BaseForm):

    class Meta:
        model = Repository
        fields = ('ssh_keys',)
