'''
Definition of the REST framework viewsets.
'''

__all__ = (
    'SimpleModelViewSet',
    'SimpleHyperlinkedModelViewSet',
)

from rest_framework.viewsets import ModelViewSet

from .serializers import SimpleModelSerializer, SimpleHyperlinkedModelSerializer


class SimpleModelViewSet(ModelViewSet):
    '''
    A REST framework `ModelViewSet` on dope, which only requires a model to
    work.

    The viewset uses a model serializer as default.
    '''
    serializer_class = SimpleModelSerializer
    fields = '__all__'

    @property
    def queryset(self):
        '''
        Return the queryset for all objects of the model.

        :return: The queryset
        :rtype: django.db.query.QuerySet
        '''
        return self._meta.model.objects.all()  # pylint: disable=no-member

    @property
    def serializer_kwargs(self):
        '''
        Return the kwargs for initializing the serializer class / instance.

        :return: The keyword arguments for the serializer
        :rtype: dict
        '''
        if not issubclass(self.serializer_class, SimpleModelSerializer):
            return {}

        return {
            'model': self.model,    # pylint: disable=no-member
            'fields': self.fields,
        }

    def get_serializer(self, *args, **kwargs):
        '''
        Return the instantiated serializer.

        :return: The serializer instance
        :rtype: rest_framework.serializers.Serializer
        '''
        kwargs.update(self.serializer_kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        '''
        Return the defined serializer class per viewset method.

        return a serializer class based on action

        self.viewset_serializer_class = {
                'list' : MyListSerializer,
                'create' : MyCreateSerializer
        }

        :return: The serializer class
        :rtype: string
        '''

        # pylint: disable=no-member

        serializer = super().get_serializer_class()
        if hasattr(self, 'viewset_serializer_class') and isinstance(self.viewset_serializer_class, dict):  # pylint: disable=line-too-long
            if self.action in self.viewset_serializer_class.keys():
                serializer = self.viewset_serializer_class[self.action]
        return serializer


class SimpleHyperlinkedModelViewSet(SimpleModelViewSet):
    '''
    A REST framework `ModelViewSet` on dope, which only requires a model to
    work.

    The viewset uses a hyperlinked model serializer as default.
    '''
    serializer_class = SimpleHyperlinkedModelSerializer
