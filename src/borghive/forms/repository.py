from borghive.forms.base import BaseForm
from borghive.models import Repository


class RepositoryForm(BaseForm):
    """
    form to create repository
    """

    class Meta:
        model = Repository
        fields = ('name', 'ssh_keys', 'append_only_keys', 'location', 'alert_after_days', 'group', 'mode')
