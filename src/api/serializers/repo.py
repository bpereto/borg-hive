from django.contrib.auth.models import Group
from rest_framework import serializers

from api.lib.serializers import SimpleHyperlinkedModelSerializer
from api.serializers.key import SSHPublickeySerializer
from api.serializers.user import SimpleGroupSerializer, SimpleOwnerSerializer
from borghive.models import (Repository, RepositoryEvent, RepositoryLocation,
                             RepositoryStatistic, RepositoryUser)
from borghive.models.key import SSHPublicKey


class RepositorySerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for repository

    to selectively display fields use the deifned serializers
    """

    owner = SimpleOwnerSerializer(read_only=True)
    group = SimpleGroupSerializer(many=True, read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        source='group', queryset=Group.objects.all(), write_only=True, many=True, required=False)

    location = SimpleHyperlinkedModelSerializer(
        model=RepositoryLocation, fields='__all__', read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        source='location', queryset=RepositoryLocation.objects.all(), write_only=True)

    repo_user = SimpleHyperlinkedModelSerializer(
        model=RepositoryUser, fields='__all__', read_only=True)

    ssh_keys = SSHPublickeySerializer(many=True, read_only=True)
    ssh_keys_id = serializers.PrimaryKeyRelatedField(
        source='ssh_keys', queryset=SSHPublicKey.objects.all(), write_only=True, many=True, required=False)

    append_only_keys = SSHPublickeySerializer(many=True, read_only=True)
    append_only_keys_id = serializers.PrimaryKeyRelatedField(
        source='append_only_keys', queryset=SSHPublicKey.objects.all(), write_only=True, many=True, required=False)

    def create(self, validated_data, *args, **kwargs):
        """
        override create method to generate repository user
        and set requester as owner
        """
        repo_user = RepositoryUser()
        repo_user.save()
        validated_data['repo_user'] = repo_user
        validated_data['owner'] = self.context['request'].user
        print(validated_data['owner'])
        return super().create(validated_data, *args, **kwargs)

    class Meta:
        model = Repository
        exclude = ['last_updated', 'last_access']


class SimpleRepositorySerializer(SimpleHyperlinkedModelSerializer):
    """
    show only limited fields on repository
    """


class RepositoryEventSerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for repository event
    """

    repo = RepositorySerializer(read_only=True)

    class Meta:
        model = RepositoryEvent
        fields = '__all__'


class RepositoryStatisticSerializer(SimpleHyperlinkedModelSerializer):
    """
    serializer for repository event
    """

    repo = RepositorySerializer(read_only=True)

    class Meta:
        model = RepositoryStatistic
        fields = '__all__'
