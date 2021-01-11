from django.db import models
from django.db.models import Q


class OwnerOrGroupManager(models.Manager):
    """
    model manager for filtering by owner or group
    """

    # pylint: disable=R0903

    def by_owner_or_group(self, user):
        """
        use Django Q to filter by owner or group of user
        """
        return self.get_queryset().filter(Q(owner=user) | Q(group__in=user.groups.all()))
