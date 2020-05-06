from django.apps import apps, AppConfig
from django.contrib import admin


class BorgHiveConfig(AppConfig):
    name = 'borghive'

    def ready(self):
        import borghive.signals
        
        models = apps.get_models()
        for model in models:
            try:
                admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass
