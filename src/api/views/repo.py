import logging

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response

from api.lib.viewsets import SimpleHyperlinkedModelViewSet
from api.router import router
from api.serializers import RepositorySerializer, RepositoryEventSerializer, RepositoryStatisticSerializer
from borghive.models import Repository, RepositoryLocation, RepositoryUser, RepositoryEvent, RepositoryStatistic

LOGGER = logging.getLogger(__name__)

__all__ = ['RepositoryViewSet']


class RepositoryViewSet(SimpleHyperlinkedModelViewSet):
    """
    repository viewset
    """

    # pylint: disable=unused-argument

    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    model = Repository

    def get_queryset(self):
        return Repository.objects.by_owner_or_group(self.request.user)

    @action(methods=['get'], detail=True)
    def events(self, request, pk=None):
        """
        detail view on repository events
        """
        events = self.get_object().repositoryevent_set.all()
        serializer = RepositoryEventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def statistics(self, request, pk=None):
        """
        detail view on repository statistics
        """
        stats = self.get_object().repositorystatistic_set.all()
        serializer = RepositoryStatisticSerializer(stats, many=True, context={'request': request})
        return Response(serializer.data)


class RepositoryUserViewSet(SimpleHyperlinkedModelViewSet):
    """
    repositoryuser viewset
    """
    queryset = RepositoryUser.objects.all()
    model = RepositoryUser

    def get_queryset(self):
        return RepositoryUser.objects.filter(Q(repository__owner=self.request.user) | Q(repository__group__in=self.request.user.groups.all()))


class RepositoryEventViewSet(SimpleHyperlinkedModelViewSet):
    """
    repositoryevent viewset
    """
    queryset = RepositoryEvent.objects.all()
    serializer_class = RepositoryEventSerializer
    model = RepositoryEvent

    def get_queryset(self):
        return RepositoryEvent.objects.filter(Q(repo__owner=self.request.user) | Q(repo__group__in=self.request.user.groups.all()))


class RepositoryStatisticViewSet(SimpleHyperlinkedModelViewSet):
    """
    repositorystatistic viewset
    """
    queryset = RepositoryStatistic.objects.all()
    serializer_class = RepositoryStatisticSerializer
    model = RepositoryStatistic

    def get_queryset(self):
        return RepositoryStatistic.objects.filter(Q(repo__owner=self.request.user) | Q(repo__group__in=self.request.user.groups.all()))


class RepositoryLocationViewSet(SimpleHyperlinkedModelViewSet):
    """
    repositorylocation viewset
    """
    queryset = RepositoryLocation.objects.all()
    model = RepositoryLocation


router.register('repositories', RepositoryViewSet)
router.register('repository-users', RepositoryUserViewSet)
router.register('repository-events', RepositoryEventViewSet)
router.register('repository-statistics', RepositoryStatisticViewSet)
router.register('locations', RepositoryLocationViewSet)

# for view in map(__module__.__dict__.get, __all__):
#     LOGGER.debug('registering view: %s', view)
#     router.register(view.model._meta.verbose_name_plural.lower(), view)
