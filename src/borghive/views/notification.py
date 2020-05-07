from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.views.generic.list import ListView

from borghive.forms import AlertPreference
from borghive.models import EmailNotification


class NotificationListView(ListView):
    """
    notification list and alert preference
    """

    # pylint: disable=too-many-ancestors

    template_name = 'borghive/notification_list.html'

    def get_context_data(self, *args, **kwargs):
        """get context for notification list"""
        context = super().get_context_data(*args, **kwargs)
        alert_preference = self.request.user.alertpreference
        context['alert_preference_form'] = AlertPreference(
            instance=alert_preference)
        return context

    def get_queryset(self):
        """get all configured notification type objects"""
        return EmailNotification.objects.all()

    def post(self, request):
        """handle alert preference update"""

        if 'alert-pref' in self.request.POST:
            obj = request.user.alertpreference
            alert_preference = AlertPreference(data=request.POST, instance=obj)
            if alert_preference.is_valid():
                alert_preference.save()
                messages.add_message(
                    self.request, messages.SUCCESS, "Alert preference saved")
            else:
                messages.add_message(
                    self.request, messages.ERROR, "Alert preference save failed")

        return redirect(reverse('notification-list'))
