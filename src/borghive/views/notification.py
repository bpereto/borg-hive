from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from borghive.forms import (AlertPreferenceForm, NotificationCreateForm, NotificationUpdateForm)
from borghive.mixins import OwnerFilterMixin
from borghive.models import EmailNotification

# pylint: disable=protected-access


class NotificationListView(OwnerFilterMixin, ListView):
    """
    notification list and alert preference
    """

    # pylint: disable=too-many-ancestors

    template_name = 'borghive/notification_list.html'
    queryset = EmailNotification.objects.all()

    def get_context_data(self, *args, **kwargs):
        """get context for notification list"""
        context = super().get_context_data(*args, **kwargs)
        alert_preference = self.request.user.alertpreference
        context['alert_preference_form'] = AlertPreferenceForm(
            instance=alert_preference)
        return context

    def post(self, request):
        """handle alert preference update"""

        if 'alert-pref' in self.request.POST:
            obj = request.user.alertpreference
            alert_preference = AlertPreferenceForm(
                data=request.POST, instance=obj)
            if alert_preference.is_valid():
                alert_preference.save()
                messages.add_message(
                    self.request, messages.SUCCESS, "Alert preference saved")
            else:
                messages.add_message(
                    self.request, messages.ERROR, "Alert preference save failed")

        return redirect(reverse('notification-list'))


class NotificationDetailView(OwnerFilterMixin, DetailView):
    """ssh public key detail"""

    model = EmailNotification


class NotificationDeleteView(OwnerFilterMixin, DeleteView):
    """ssh public key delete"""

    model = EmailNotification
    success_url = reverse_lazy('notification-list')
    template_name = 'borghive/notification_delete.html'


class NotificationUpdateView(OwnerFilterMixin, UpdateView):
    """ssh public key update - handle parse errors"""

    model = EmailNotification
    success_url = reverse_lazy('notification-list')
    form_class = NotificationUpdateForm
    template_name = 'borghive/notification_update.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             'Updated notification: {}'.format(form.instance.email))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form._errors:
            message = ''
            for msg in form._errors[field]:
                message += '<p>' + msg + '</p>'
            messages.add_message(self.request, messages.ERROR, message)
        return redirect(reverse('notification-list'))


class NotificationCreateView(OwnerFilterMixin, CreateView):
    """notification create view - handle parse errors"""

    model = EmailNotification
    form_class = NotificationCreateForm
    template_name = 'borghive/notification_create.html'

    def get_success_url(self):
        return reverse('notification-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             'Added notification: {}'.format(form.instance.email))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form._errors:
            message = ''
            for msg in form._errors[field]:
                message += '<p>' + msg + '</p>'
            messages.add_message(self.request, messages.ERROR, message)
        return redirect(reverse('notification-list'))
