from django.contrib.auth.models import Group, User

from api.lib.serializers import SimpleHyperlinkedModelSerializer


class SimpleOwnerSerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for owner aka user
    limited to not expose to much information
    """

    class Meta:
        model = User
        fields = ('id', 'username',)


class SimpleGroupSerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for group
    """

    class Meta:
        model = Group
        fields = ('id', 'name',)
