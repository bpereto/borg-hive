'''
Definition of the REST framework serializers.
'''

__all__ = (
    'SimpleModelSerializer',
    'SimpleHyperlinkedModelSerializer',
)

from drf_queryfields import QueryFieldsMixin
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        HyperlinkedRelatedField,
                                        ModelSerializer, ReadOnlyField)
from rest_framework.utils.field_mapping import get_nested_relation_kwargs

# pylint: disable=redefined-builtin

NAMESPACE = 'api'


class SimpleModelSerializer(QueryFieldsMixin, ModelSerializer):  # pylint: disable=too-few-public-methods
    '''
    A REST framework `ModelSerializer` on dope, which automatically initializes
    the Meta class of the serializer, based on the arguments provided in the
    constructor.
    '''
    namespace = NAMESPACE

    def __init__(self, *args, model=None, fields=None, **kwargs):
        '''
        Initialize the Meta class before initializing the serializer.
        '''

        if not hasattr(self, 'Meta'):
            self.Meta = type('Meta', (), {'model': model, 'fields': fields})  # pylint: disable=invalid-name

        super().__init__(*args, **kwargs)

    def build_url_field(self, field_name, model_class):
        '''
        Create a field representing the object's own URL.

        Please note this method is overloaded to add the namespace to the view
        name.
        '''
        field_class, field_kwargs = super().build_url_field(field_name, model_class)
        field_kwargs['view_name'] = '{}:{}'.format(self.namespace, field_kwargs['view_name'])
        return field_class, field_kwargs

    def build_relational_field(self, field_name, relation_info):
        field_class, field_kwargs = super().build_relational_field(field_name, relation_info)

        if hasattr(field_kwargs, 'view_name'):
            field_kwargs['view_name'] = '{}:{}'.format(self.namespace, field_kwargs['view_name'])

        return field_class, field_kwargs


class SimpleHyperlinkedRelatedField(HyperlinkedRelatedField):
    """
    A REST framework `HyperlinkedRelatedField` to support namespaces
    """

    namespace = NAMESPACE

    def __init__(self, *args, **kwargs):
        kwargs['view_name'] = self.namespace + ':' + kwargs['view_name']
        super().__init__(*args, **kwargs)


class SimpleHyperlinkedModelSerializer(SimpleModelSerializer, HyperlinkedModelSerializer):  # pylint: disable=too-few-public-methods
    '''
    A REST framework `HyperlinkedModelSerializer` on dope, which automatically
    initializes the Meta class of the serializer, based on the arguments
    provided in the constructor.
    '''
    serializer_related_field = SimpleHyperlinkedRelatedField

    id = ReadOnlyField()

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.
        """
        class NestedSerializer(SimpleHyperlinkedModelSerializer):  # pylint: disable=too-few-public-methods,missing-docstring
            class Meta:  # pylint: disable=too-few-public-methods,missing-docstring
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = '__all__'

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs
