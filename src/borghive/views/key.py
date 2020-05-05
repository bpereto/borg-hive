from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from borghive.models import SSHPublicKey
from borghive.forms import SSHPublicKeyCreateForm, SSHPublicKeyUpdateForm
from borghive.mixins import OwnerFilterMixin


class SSHPublicKeyListView(OwnerFilterMixin, ListView):

    model = SSHPublicKey
    template_name = 'borghive/key_list.html'


class SSHPublicKeyDetailView(OwnerFilterMixin, DetailView):

    model = SSHPublicKey


class SSHPublicKeyDeleteView(OwnerFilterMixin, DeleteView):

    model = SSHPublicKey
    success_url = reverse_lazy('key-list')
    template_name = 'borghive/key_delete.html'


class SSHPublicKeyUpdateView(OwnerFilterMixin, UpdateView):

    model = SSHPublicKey
    success_url = reverse_lazy('key-list')
    form_class = SSHPublicKeyUpdateForm
    template_name = 'borghive/key_update.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Updated SSH-Key: {}'.format(form.instance.name))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form._errors:
            message = ''
            for msg in form._errors[field]:
                message += '<p>' + msg + '</p>'
            messages.add_message(self.request, messages.ERROR, message)
        return redirect(reverse('key-list'))


class SSHPublicKeyCreateView(OwnerFilterMixin, CreateView):

    model = SSHPublicKey
    form_class = SSHPublicKeyCreateForm
    template_name = 'borghive/key_create.html'

    def get_success_url(self):
        return reverse('key-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.add_message(self.request, messages.SUCCESS, 'Added SSH-Key: {}'.format(form.instance.name))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form._errors:
            message = ''
            for msg in form._errors[field]:
                message += '<p>' + msg + '</p>'
            messages.add_message(self.request, messages.ERROR, message)
        return redirect(reverse('key-list'))
