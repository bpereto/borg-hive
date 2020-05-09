import logging

from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField

LOGGER = logging.getLogger(__name__)


class BaseForm(forms.ModelForm):
    '''
    base form to handle complex owner filter
    '''

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field_type in self.fields.items():
            if isinstance(field_type, (ModelMultipleChoiceField, ModelChoiceField)):
                model = field_type._queryset.model
                LOGGER.debug('model: %s', model)
                LOGGER.debug(field_type)
                LOGGER.debug(field_name)
                try:
                    if model._meta.get_field('owner') and owner and user:
                        LOGGER.debug('field: owner - filtering')
                        self.fields[field_name].queryset = model.objects.filter(
                            Q(owner=owner) | Q(group__in=user.groups.all()))
                except FieldDoesNotExist:
                    pass
                try:
                    if model == Group and user:
                        LOGGER.debug('field: group - filtering')
                        print(user.groups.all())
                        self.fields[field_name].queryset = user.groups.all()
                except FieldDoesNotExist:
                    pass
                LOGGER.debug(self.fields[field_name].queryset)

    class Meta:
        abstract = True
