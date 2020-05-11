from borghive.forms.base import BaseForm
from borghive.models import EmailNotification, PushoverNotification


class EmailNotificationForm(BaseForm):
    """
    form for a email notification
    """

    class Meta:
        model = EmailNotification
        fields = ('email', 'group',)


class PushoverNotificationForm(BaseForm):
    """
    form for a pushover notification
    """

    class Meta:
        model = PushoverNotification
        fields = ('name', 'user', 'token', 'group',)
