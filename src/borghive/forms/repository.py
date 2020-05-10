from borghive.forms.base import BaseForm
from borghive.models import Repository


class RepositoryCreateForm(BaseForm):
    """
    form to create repository
    """

    class Meta:
        model = Repository
        fields = ('name', 'ssh_keys', 'alert_after_days', 'group',)


class RepositoryUpdateForm(BaseForm):
    """
    form to update repository
    """

    class Meta:
        model = Repository
        fields = ('ssh_keys', 'alert_after_days', 'group',)
