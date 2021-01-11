from rest_framework import serializers
from django.contrib.auth.models import Group

from api.lib.serializers import SimpleHyperlinkedModelSerializer
from api.serializers.user import SimpleGroupSerializer, SimpleOwnerSerializer
from borghive.models import SSHPublicKey


class SSHPublickeySerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for ssh public key
    """

    type = serializers.CharField(read_only=True)
    bits = serializers.IntegerField(read_only=True)
    fingerprint = serializers.CharField(read_only=True)
    comment = serializers.CharField(read_only=True)

    owner = SimpleOwnerSerializer(read_only=True, default=serializers.CurrentUserDefault())
    group = SimpleGroupSerializer(many=True, read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(source='group', queryset=Group.objects.all(), write_only=True, many=True, required=False)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = SSHPublicKey
        fields = '__all__'
