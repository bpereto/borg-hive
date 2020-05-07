from django import forms
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField


class BaseForm(forms.ModelForm):
    '''
    base form to handle complex owner filter
    '''

    def __init__(self, owner=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_type in self.fields.items():
            if type(field_type) == ModelMultipleChoiceField or type(field_type) == ModelChoiceField:
                model = field_type._queryset.model
                try:
                    if model._meta.get_field('owner'):
                        self.fields[field_name].queryset = model.objects.filter(
                            owner=owner)
                except FieldDoesNotExist:
                    pass

    class Meta:
        abstract = True
