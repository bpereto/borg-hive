from django.db.models.signals import post_save
from django.dispatch import receiver
from borghive.models import RepositoryUser
import borghive.tasks

@receiver(post_save, sender=RepositoryUser)
def repository_user_created(sender, instance, created, **kwargs):
    print('create repo user')
    print(created)
    if created:
        borghive.tasks.create_repo_user(instance.id)
