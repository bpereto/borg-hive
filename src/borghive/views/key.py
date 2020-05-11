from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from borghive.forms import SSHPublicKeyForm
from borghive.mixins import OwnerFilterMixin
from borghive.models import SSHPublicKey

# pylint: disable=too-many-ancestors,protected-access


class SSHPublicKeyListView(OwnerFilterMixin, ListView):
    """ssh public key list"""

    model = SSHPublicKey
    template_name = 'borghive/key_list.html'


class SSHPublicKeyDetailView(OwnerFilterMixin, DetailView):
    """ssh public key detail"""

    model = SSHPublicKey


class SSHPublicKeyDeleteView(OwnerFilterMixin, DeleteView):
    """ssh public key delete"""

    model = SSHPublicKey
    success_url = reverse_lazy('key-list')
    template_name = 'borghive/key_delete.html'


class SSHPublicKeyUpdateView(OwnerFilterMixin, UpdateView):
    """ssh public key update - handle parse errors"""

    model = SSHPublicKey
    success_url = reverse_lazy('key-list')
    form_class = SSHPublicKeyForm
    template_name = 'borghive/key_update.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             'Updated SSH-Key: {}'.format(form.instance.name))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form._errors:
            message = ''
            for msg in form._errors[field]:
                message += '<p>' + msg + '</p>'
            messages.add_message(self.request, messages.ERROR, message)
        return redirect(reverse('key-list'))


class SSHPublicKeyCreateView(OwnerFilterMixin, CreateView):
    """ssh public key create view - handle parse errors"""

    model = SSHPublicKey
    form_class = SSHPublicKeyForm
    template_name = 'borghive/key_create.html'

    def get_success_url(self):
        return reverse('key-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.add_message(self.request, messages.SUCCESS,
                             'Added SSH-Key: {}'.format(form.instance.name))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form._errors:
            message = ''
            for msg in form._errors[field]:
                message += '<p>' + msg + '</p>'
            messages.add_message(self.request, messages.ERROR, message)
        return redirect(reverse('key-list'))
