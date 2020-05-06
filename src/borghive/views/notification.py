from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from borghive.models import EmailNotification
from borghive.mixins import OwnerFilterMixin
from borghive.forms import AlertPreference


class NotificationListView(ListView):

    template_name = 'borghive/notification_list.html'

    def get_context_data(self):
        context = super().get_context_data()
        alert_preference = self.request.user.alertpreference
        context['alert_preference_form'] = AlertPreference(instance=alert_preference)
        return context

    def get_queryset(self):
        return EmailNotification.objects.all()

    def post(self, request):

        if 'alert-pref' in self.request.POST:
            obj = request.user.alertpreference
            alert_preference = AlertPreference(data=request.POST, instance=obj)
            if alert_preference.is_valid():
                alert_preference.save()
                messages.add_message(self.request, messages.SUCCESS, "Alert preference saved")
            else:
                messages.add_message(self.request, messages.ERROR, "Alert preference save failed")

            return redirect(reverse('notification-list'))
