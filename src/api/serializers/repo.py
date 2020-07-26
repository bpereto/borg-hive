from api.lib.serializers import SimpleHyperlinkedModelSerializer
from api.serializers.key import SSHPublickeySerializer
from api.serializers.user import SimpleGroupSerializer, SimpleOwnerSerializer
from borghive.models import (Repository, RepositoryLocation, RepositoryUser)


class RepositorySerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for repository

    to selectively display fields use the deifned serializers
    """

    owner = SimpleOwnerSerializer()
    group = SimpleGroupSerializer(many=True)

    location = SimpleHyperlinkedModelSerializer(model=RepositoryLocation, fields='__all__')
    repo_user = SimpleHyperlinkedModelSerializer(model=RepositoryUser, fields='__all__')

    ssh_keys = SSHPublickeySerializer(many=True)
    append_only_keys = SSHPublickeySerializer(many=True)

    class Meta:
        model = Repository
        fields = '__all__'
