from borghive.forms.base import BaseForm
from borghive.models import Repository


class RepositoryForm(BaseForm):
    """
    form to create repository
    """

    class Meta:
        model = Repository
        fields = ('name', 'ssh_keys', 'alert_after_days', 'group',)
