from django.apps import AppConfig, apps
from django.contrib import admin


class BorgHiveConfig(AppConfig):
    """borghive app config"""

    name = 'borghive'

    def ready(self):
        """initialize borghive config"""
        import borghive.signals  # pylint: disable=unused-import,import-outside-toplevel
        import borghive.lib.rules  # pylint: disable=unused-import,import-outside-toplevel

        models = apps.get_models()
        for model in models:
            try:
                admin.site.register(model)
            except admin.sites.AlreadyRegistered:
                pass
