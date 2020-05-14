import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import borghive.tasks
from borghive.models import Repository, RepositoryEvent, RepositoryUser, RepositoryLdapUser, AlertPreference

LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """create alert preference when a user is created"""
    if created:
        AlertPreference.objects.create(user=instance)


@receiver(post_save, sender=RepositoryUser)
def repository_user_created(sender, instance, created, **kwargs):
    """sync repositoryuser to ldap sshd when a user is created"""
    LOGGER.debug('repository_user_created: %s, %s, %s, %s',
                 sender, instance, created, kwargs)
    instance.sync_to_ldap()


@receiver(post_delete, sender=RepositoryUser)
def repository_user_deleted(sender, instance, **kwargs):
    """delete ldap user for sshd when a repo user is deleted"""
    LOGGER.debug('repository_user_deleted: %s, %s, %s',
                 sender, instance, kwargs)
    try:
        RepositoryLdapUser.objects.get(username=instance.name).delete()
    except RepositoryLdapUser.DoesNotExist:
        pass

@receiver(post_delete, sender=Repository)
def repository_deleted(sender, instance, **kwargs):
    """delete repository data on filesystem when repository is deleted"""
    LOGGER.debug('repository_deleted: %s, %s, %s',
                 sender, instance, kwargs)
    borghive.tasks.repository_delete.delay(instance.get_repo_path())


@receiver(post_save, sender=RepositoryEvent)
def handle_repository_event(sender, instance, created, **kwargs):
    """filter emitted repository events and take actions"""

    LOGGER.debug('handle_repository_event: %s, %s, %s, %s',
                 sender, instance, created, kwargs)

    LOGGER.debug(instance.event_type)
    LOGGER.debug(instance.message)

    # shaky: repository updated / archive created
    if created and instance.event_type == RepositoryEvent.WATCHER and 'Repository updated' in instance.message:
        borghive.tasks.create_repo_statistic.delay(repo_id=instance.repo.id)
