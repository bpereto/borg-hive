from rest_framework import serializers
from django.contrib.auth.models import Group

from api.lib.serializers import SimpleHyperlinkedModelSerializer
from api.serializers.user import SimpleGroupSerializer, SimpleOwnerSerializer
from borghive.models import SSHPublicKey


class SSHPublickeySerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for ssh public key
    """

    owner = SimpleOwnerSerializer(read_only=True)
    group = SimpleGroupSerializer(many=True, read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(source='group', queryset=Group.objects.all(), write_only=True, many=True, required=False)

    class Meta:
        model = SSHPublicKey
        fields = '__all__'
