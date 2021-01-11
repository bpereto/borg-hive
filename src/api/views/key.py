import logging

from api.lib.viewsets import SimpleHyperlinkedModelViewSet
from api.router import router
from api.serializers.key import SSHPublickeySerializer
from borghive.models import SSHPublicKey

LOGGER = logging.getLogger(__name__)

__all__ = ['SSHPublicKeyViewSet']


class SSHPublicKeyViewSet(SimpleHyperlinkedModelViewSet):
    """
    SSH-Publickey Viewset
    """
    queryset = SSHPublicKey.objects.all()
    serializer_class = SSHPublickeySerializer
    model = SSHPublicKey

    def get_queryset(self):
        return SSHPublicKey.objects.by_owner_or_group(self.request.user)


router.register('sshpublickeys', SSHPublicKeyViewSet)

# for view in map(__module__.__dict__.get, __all__):
#     LOGGER.debug('registering view: %s', view)
#     router.register(view.model._meta.verbose_name_plural.lower(), view)
