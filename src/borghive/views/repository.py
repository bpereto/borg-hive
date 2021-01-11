import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from borghive.views.base import BaseView
from borghive.forms import RepositoryForm
from borghive.lib.keys import get_ssh_host_key_infos
from borghive.models import Repository, RepositoryUser
import borghive.exceptions


LOGGER = logging.getLogger(__name__)


class RepositoryListView(BaseView, ListView):
    """repository list"""

    model = Repository

    def get_total_usage(self):  # pylint: disable=no-self-use
        """get total usage from repostatistic of all repos"""
        total_size = 0
        for repo in Repository.objects.by_owner_or_group(user=self.request.user):
            stat = repo.get_last_repository_statistic()
            if stat:
                total_size += stat.repo_size
        return total_size

    def get_context_data(self, **kwargs):
        """get context for repositories"""
        context = super().get_context_data(**kwargs)
        context['current_total_usage'] = self.get_total_usage()
        return context


class RepositoryDetailView(BaseView, DetailView):
    """repository details"""

    model = Repository

    def chart_data_usage(self):
        '''
        convert repository statistic to chartjs data
        use resolution to calculate average repo size
        '''
        labels = []
        data = []

        for stat in self.object.repositorystatistic_set.all():
            labels.append(stat.created.isoformat())
            data.append(stat.repo_size)

        return {'chart_repo_usage_data': data, 'chart_repo_usage_labels': labels, 'chart_date_format': settings.DATETIME_FORMAT}

    def get_context_data(self, **kwargs):
        """get context for repository detail"""
        context = super().get_context_data(**kwargs)
        context.update(self.chart_data_usage())
        context['key_info'] = get_ssh_host_key_infos()
        context['events'] = self.object.repositoryevent_set.order_by(
            '-created')
        return context

    def post(self, request, pk):
        """handle refresh for repository"""
        if 'refresh' in request.POST:
            repo = Repository.objects.get(id=pk)
            try:
                repo.refresh()
            except borghive.exceptions.RepositoryNotCreated:
                messages.add_message(self.request, messages.WARNING, "Repository not yet initialized.")
        return redirect(reverse('repository-detail', args=[pk]))


class RepositoryUpdateView(BaseView, UpdateView):
    """repository update"""

    model = Repository
    success_url = reverse_lazy('repository-list')
    form_class = RepositoryForm
    template_name = 'borghive/repository_update.html'


class RepositoryDeleteView(BaseView, DeleteView):
    """repository delete"""

    model = Repository
    success_url = reverse_lazy('repository-list')
    template_name = 'borghive/repository_delete.html'


class RepositoryCreateView(BaseView, CreateView):
    """repository create"""

    model = Repository
    form_class = RepositoryForm
    template_name = 'borghive/repository_create.html'

    def get_success_url(self):
        """redirect url"""
        return reverse('repository-detail', args=[self.object.id])

    def form_valid(self, form):
        """handle form valid"""
        repo_user = RepositoryUser()
        repo_user.save()
        form.instance.repo_user = repo_user
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        """handle from invalid"""
        messages.add_message(self.request, messages.ERROR, "Form is invalid")
        return redirect(reverse('repository-list'))
