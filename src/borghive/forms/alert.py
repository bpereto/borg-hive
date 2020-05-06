from django import forms
from crispy_forms.helper import FormHelper

from borghive.models import AlertPreference
from borghive.forms import BaseForm


class AlertPreference(BaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.fields['alert_interval'].help_text = 'After which interval (hours) you will be notified again'
        self.fields['alert_expiration'].help_text = 'After how many days you will not receive any notification (even if backup is in bad state)'


    class Meta:
        model = AlertPreference
        fields = ('alert_interval', 'alert_expiration',)
        exclude = ('user',)
