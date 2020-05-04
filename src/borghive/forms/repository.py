from django import forms

from borghive.models import Repository


class RepositoryCreateForm(forms.ModelForm):


    class Meta:
        model = Repository
        fields = '__all__'
        exclude = ('repo_user',)


class RepositoryUpdateForm(forms.ModelForm):

    class Meta:
        model = Repository
        fields = ('ssh_keys',)
