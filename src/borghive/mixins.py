
class OwnerFilterMixin:
    """mixin to filter querysets for owner"""

    def get_queryset(self):
        """filter owner"""
        return super().get_queryset().filter(owner=self.request.user)

    def get_form_kwargs(self):
        """pass owner to forms"""
        kwargs = super().get_form_kwargs()
        kwargs.update({'owner': self.request.user})
        return kwargs
