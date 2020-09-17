from django.db import models
from django.db.models import Q

class OwnerOrGroupManager(models.Manager):

    def by_owner_or_group(self, user):
        return self.get_queryset().filter(Q(owner=user) | Q(group__in=user.groups.all()))