from django import forms
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.core.exceptions import FieldDoesNotExist


class BaseForm(forms.ModelForm):
    '''
    base form to handle complex owner filter
    '''

    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_type in self.fields.items():
            if isinstance(field_type, (ModelMultipleChoiceField, ModelChoiceField)):
                model = field_type._queryset.model
                try:
                    if model._meta.get_field('owner'):
                        self.fields[field_name].queryset = model.objects.filter(
                            owner=owner)
                except FieldDoesNotExist:
                    pass

    class Meta:
        abstract = True
