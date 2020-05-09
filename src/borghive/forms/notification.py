
from borghive.forms.base import BaseForm
from borghive.models import EmailNotification


class NotificationCreateForm(BaseForm):
    """
    form to create a notification
    """

    class Meta:
        model = EmailNotification
        fields = ('email',)


class NotificationUpdateForm(BaseForm):
    """
    form to update notification
    """

    class Meta:
        model = EmailNotification
        fields = ('email',)
