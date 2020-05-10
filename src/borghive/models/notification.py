import logging

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core import mail
from django.core.validators import MaxValueValidator
from django.db import models

from borghive.models.base import BaseModel

LOGGER = logging.getLogger(__name__)


class NotificationBase(BaseModel):
    """
    notifcation base class for notification types
    email, pushover, get/post webhooks
    """

    def notify(self, *args, **kwargs):
        '''
        execute notification
        '''
        raise NotImplementedError()

    class Meta():
        abstract = True


class AlertPreference(models.Model):
    """
    alert preference per user/owner
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alert_interval = models.PositiveIntegerField(
        default=12, validators=[MaxValueValidator(48)])  # in hours
    alert_expiration = models.PositiveIntegerField(
        default=5, validators=[MaxValueValidator(30)])  # in days


class EmailNotification(BaseModel):
    """
    email notification
    """
    email = models.EmailField()
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    group = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return 'EmailNotification: {}'.format(self.email)

    def notify(self, subject, message):
        """send email"""
        LOGGER.debug('send email notification: "%s" to %s',
                     subject, self.email)

        mail.send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[self.email],
            fail_silently=False
        )
