
from borghive.forms import BaseForm
from borghive.models import Repository


class RepositoryCreateForm(BaseForm):

    class Meta:
        model = Repository
        fields = '__all__'
        exclude = ('repo_user', 'owner')


class RepositoryUpdateForm(BaseForm):

    class Meta:
        model = Repository
        fields = ('ssh_keys', 'alert_after_days',)
