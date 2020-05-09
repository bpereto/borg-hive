from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from rules.contrib.views import AutoPermissionRequiredMixin

from borghive.mixins import OwnerFilterMixin

# pylint: disable=too-few-public-methods


class BaseView(AutoPermissionRequiredMixin, OwnerFilterMixin):
    """
    base view class to all views
    defines some basics
    """

    permission_type_map = [
        (CreateView, 'add'),
        (UpdateView, 'change'),
        (DeleteView, 'delete'),
        (DetailView, 'view'),
        (ListView, 'list'),
    ]

    def get_form_kwargs(self):
        """add request.user to form kwargs"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})  # pylint: disable=no-member
        return kwargs

    class Meta:
        """meta"""
        abstract = True
