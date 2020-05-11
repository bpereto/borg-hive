from django.contrib import admin
from borghive.models import EmailNotification, PushoverNotification


class NotifyAdmin(admin.ModelAdmin):

    actions = ['test_notify', ]

    def test_notify(self, request, queryset):
        for notification in queryset:
            notification.notify(**notification.get_test_params())
        
    test_notify.short_description = "Test Notification"


admin.site.register(EmailNotification, NotifyAdmin)
admin.site.register(PushoverNotification, NotifyAdmin)
