from api.lib.serializers import SimpleHyperlinkedModelSerializer
from api.serializers.user import SimpleGroupSerializer, SimpleOwnerSerializer
from borghive.models import SSHPublicKey


class SSHPublickeySerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for ssh public key
    """

    owner = SimpleOwnerSerializer()
    group = SimpleGroupSerializer(many=True)

    class Meta:
        model = SSHPublicKey
        fields = '__all__'
