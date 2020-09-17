import logging

from django.db.models import Q

from api.lib.viewsets import SimpleHyperlinkedModelViewSet
from api.router import router
from api.serializers import RepositorySerializer
from borghive.models import Repository, RepositoryLocation, RepositoryUser

LOGGER = logging.getLogger(__name__)

__all__ = ['RepositoryViewSet']


class RepositoryViewSet(SimpleHyperlinkedModelViewSet):
    """
    repository viewset
    """
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    model = Repository

    def get_queryset(self):
        return Repository.objects.by_owner_or_group(self.request.user)


class RepositoryUserViewSet(SimpleHyperlinkedModelViewSet):
    """
    repositoryuser viewset
    """
    queryset = RepositoryUser.objects.all()
    model = RepositoryUser

    def get_queryset(self):
        return RepositoryUser.objects.filter(Q(repository__owner=self.request.user) | Q(repository__group__in=self.request.user.groups.all()))


class RepositoryLocationViewSet(SimpleHyperlinkedModelViewSet):
    """
    repositorylocation viewset
    """
    queryset = RepositoryLocation.objects.all()
    model = RepositoryLocation


router.register('repositories', RepositoryViewSet)
router.register('repository-users', RepositoryUserViewSet)
router.register('locations', RepositoryLocationViewSet)

# for view in map(__module__.__dict__.get, __all__):
#     LOGGER.debug('registering view: %s', view)
#     router.register(view.model._meta.verbose_name_plural.lower(), view)
