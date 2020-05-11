from django.contrib import admin
from borghive.models import EmailNotification, PushoverNotification

# pylint: disable=R0201


class NotifyAdmin(admin.ModelAdmin):
    """
    Admin integration for custom test notify action
    """
    actions = ['test_notify', ]

    def test_notify(self, request, queryset):
        """send test notification for each notification in queryset"""
        for notification in queryset:
            notification.notify(**notification.get_test_params())

    test_notify.short_description = "Test Notification"


admin.site.register(EmailNotification, NotifyAdmin)
admin.site.register(PushoverNotification, NotifyAdmin)
