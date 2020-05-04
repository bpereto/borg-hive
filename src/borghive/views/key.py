from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from borghive.models import SSHPublicKey
from borghive.forms import SSHPublicKeyCreateForm, SSHPublicKeyUpdateForm


class SSHPublicKeyListView(ListView):

    model = SSHPublicKey
    template_name = 'borghive/key_list.html'


class SSHPublicKeyDetailView(DetailView):

    model = SSHPublicKey


class SSHPublicKeyDeleteView(DeleteView):

    model = SSHPublicKey
    success_url = reverse_lazy('key-list')
    template_name = 'borghive/key_delete.html'


class SSHPublicKeyUpdateView(UpdateView):

    model = SSHPublicKey
    success_url = reverse_lazy('key-list')
    form_class = SSHPublicKeyUpdateForm
    template_name = 'borghive/key_update.html'


class SSHPublicKeyCreateView(CreateView):

    model = SSHPublicKey
    form_class = SSHPublicKeyCreateForm
    template_name = 'borghive/key_create.html'

    def get_success_url(self):
        return redirect(reverse('key-list'))

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Form is invalid")
        return redirect(reverse('key-list'))
