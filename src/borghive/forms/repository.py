from borghive.forms.base import BaseForm
from borghive.models import Repository


class RepositoryCreateForm(BaseForm):
    """
    form to create repository
    """

    # pylint: disable=modelform-uses-exclude

    class Meta:
        model = Repository
        fields = '__all__'
        exclude = ('repo_user', 'owner')


class RepositoryUpdateForm(BaseForm):
    """
    form to update repository
    """

    class Meta:
        model = Repository
        fields = ('ssh_keys', 'alert_after_days',)
