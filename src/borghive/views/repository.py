from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Avg
from django.utils.dateformat import format
from django.conf import settings
import logging

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from borghive.models import Repository, RepositoryUser
from borghive.forms import RepositoryCreateForm, RepositoryUpdateForm
from borghive.mixins import OwnerFilterMixin

from django.utils import timezone
import datetime

LOGGER = logging.getLogger(__name__)


class RepositoryListView(OwnerFilterMixin, ListView):

    model = Repository

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_total_usage(self):
        total_size = 0
        for repo in Repository.objects.all():
            stat = repo.get_last_repository_statistic()
            if stat:
                total_size += stat.repo_size
        return total_size

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_total_usage'] = self.get_total_usage()
        return context


class RepositoryDetailView(OwnerFilterMixin, DetailView):

    model = Repository

    def chart_data_usage(self):
        '''
        convert repository statistic to chartjs data
        use resolution to calculate average repo size
        '''
        labels = []
        data   = []

        for stat in self.object.repositorystatistic_set.all():
            labels.append(stat.created.isoformat())
            data.append(stat.repo_size)

        return {'chart_repo_usage_data': data, 'chart_repo_usage_labels': labels, 'chart_date_format': settings.DATETIME_FORMAT}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.chart_data_usage())
        return context

    def post(self, request, pk, **kwargs):

        if 'refresh' in request.POST:
            repo = Repository.objects.get(id=pk)
            repo.refresh()
        return redirect(reverse('repository-detail', args=[pk]))


class RepositoryUpdateView(OwnerFilterMixin, UpdateView):

    model = Repository
    success_url = reverse_lazy('repository-list')
    form_class = RepositoryUpdateForm
    template_name = 'borghive/repository_update.html'


class RepositoryDeleteView(OwnerFilterMixin, DeleteView):

    model = Repository
    success_url = reverse_lazy('repository-list')
    template_name = 'borghive/repository_delete.html'


class RepositoryCreateView(OwnerFilterMixin, CreateView):

    model = Repository
    form_class = RepositoryCreateForm
    template_name = 'borghive/repository_create.html'

    def get_success_url(self):
        return reverse('repository-detail', args=[self.object.id])

    def form_valid(self, form):
        repo_user = RepositoryUser()
        repo_user.save()
        form.instance.repo_user = repo_user
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Form is invalid")
        return redirect(reverse('repository-list'))
