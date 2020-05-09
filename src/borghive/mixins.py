from django.db.models import Q


class OwnerFilterMixin:
    """mixin to filter querysets for owner"""

    def get_queryset(self):
        """get only objects related to owner or same group"""
        return super().get_queryset().filter(Q(owner=self.request.user) | Q(group__in=self.request.user.groups.all()))

    def get_form_kwargs(self):
        """pass owner to forms"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'owner': self.request.user})
        return kwargs
