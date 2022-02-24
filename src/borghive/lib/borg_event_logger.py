"""
borg logger extension

patch borg to enable event logging
"""

import os
import logging
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARNING)


def log_rpc(repository, rpc_method):
    """
    log an rpc method to borg-hive
    """

    LOGGER.debug(f'repository={repository} event={rpc_method}')

    if repository:
        from django.core import management
        management.call_command("borg_event", "--event", f"{rpc_method}", "--repo-path", f"{repository.path}")