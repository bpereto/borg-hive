from django.contrib.auth.models import Group, User

from api.lib.viewsets import SimpleHyperlinkedModelViewSet
# from api.router import router
from api.serializers import SimpleGroupSerializer, SimpleOwnerSerializer

__all__ = ['UserViewset', 'GroupViewset']


class UserViewset(SimpleHyperlinkedModelViewSet):
    """
    user viewset for api
    """
    queryset = User.objects.all()
    serializer_class = SimpleOwnerSerializer
    model = User


class GroupViewset(SimpleHyperlinkedModelViewSet):
    """
    group viewset for api
    """
    queryset = Group.objects.all()
    serializer_class = SimpleGroupSerializer
    model = Group


# router.register('users', UserViewset)
# router.register('groups', GroupViewset)
