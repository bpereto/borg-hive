import logging

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


class RepositoryUserViewSet(SimpleHyperlinkedModelViewSet):
    """
    repositoryuser viewset
    """
    queryset = RepositoryUser.objects.all()
    model = RepositoryUser


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
