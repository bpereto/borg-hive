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

from django.utils import timezone
import datetime

LOGGER = logging.getLogger(__name__)


class RepositoryListView(ListView):

    model = Repository

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


class RepositoryDetailView(DetailView):

    model = Repository

    def chart_data_usage(self):
        '''
        convert repository statistic to chartjs data
        use resolution to calculate average repo size
        '''
        labels = []
        data   = []

        timetraveller = self.object.created
        now = timezone.now()

        # shift resolution depending on repo age
        if ((now - timetraveller).days <= 7):
            resolution = 1
        elif ((now - timetraveller).days <= 365):
            resolution = 7
        elif ((now - timetraveller).days > 365):
            resolution = 30

        LOGGER.debug('chart_data_usage: resolution = %s', resolution)
        while (timetraveller < now):
            timetraveller_end = timetraveller + datetime.timedelta(days=resolution)
            LOGGER.debug('chart_data_usage: get dataset from %s to %s', timetraveller, timetraveller_end)
            qs = self.object.repositorystatistic_set.filter(created__gte=timetraveller, created__lte=timetraveller_end)
            if qs:
                avg = qs.aggregate(Avg('repo_size'))
                avg_date = format(qs.first().created, settings.DATE_FORMAT)
                labels.append(avg_date)
                data.append(avg['repo_size__avg'])
                LOGGER.debug('chart_data_usage: average repo_size: %s', avg)
                LOGGER.debug('chart_data_usage: average date: %s', avg_date)
            else:
                LOGGER.debug('chart_data_usage: no data found for timeframe %s to %s', timetraveller, timetraveller_end)

            timetraveller += datetime.timedelta(days=resolution)
        return {'chart_repo_usage_data': data, 'chart_repo_usage_labels': labels}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.chart_data_usage())
        return context

    def post(self, request, pk, **kwargs):

        if 'refresh' in request.POST:
            repo = Repository.objects.get(id=pk)
            repo.refresh()
        return redirect(reverse('repository-detail', args=[pk]))


class RepositoryUpdateView(UpdateView):

    model = Repository
    success_url = reverse_lazy('repository-list')
    form_class = RepositoryUpdateForm
    template_name = 'borghive/repository_update.html'


class RepositoryDeleteView(DeleteView):

    model = Repository
    success_url = reverse_lazy('repository-list')
    template_name = 'borghive/repository_delete.html'


class RepositoryCreateView(CreateView):

    model = Repository
    form_class = RepositoryCreateForm
    template_name = 'borghive/repository_create.html'

    def get_success_url(self):
        return reverse('repository-detail', args=[self.object.id])

    def form_valid(self, form):
        repo_user = RepositoryUser()
        repo_user.save()
        form.instance.repo_user = repo_user
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Form is invalid")
        return redirect(reverse('repository-list'))
