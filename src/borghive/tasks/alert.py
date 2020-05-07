import datetime
import logging
import os

from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

from borghive.models import EmailNotification, Repository, RepositoryEvent
from core.celery import app

LOGGER = get_task_logger(__name__)


@app.task
def alert_guard_tour(repo_id=None):
    if repo_id:
        repos = Repository.objects.filter(
            id=repo_id, alert_after_days__isnull=False)
    else:
        repos = Repository.objects.filter(alert_after_days__isnull=False)

    for repo in repos:
        LOGGER.debug('alert checking: %s', repo)
        if repo.should_alert():
            delta = timezone.now() - repo.last_updated
            LOGGER.warning(
                'Alert: %s last backup was %s days ago', repo, delta.days)
            repo.alert()


@app.task
def fire_alert(repo_id, alert_id):
    '''
    fire outdated backup alert
    '''
    repo = Repository.objects.get(id=repo_id)
    alert = RepositoryEvent.objects.get(id=alert_id)
    owner = repo.owner

    notifications = EmailNotification.objects.filter(owner=owner)
    LOGGER.debug('found notifications: %s', notifications)

    subject = 'Missing backup for {}'.format(repo.name)
    message = alert.message
    for messenger in notifications:
        messenger.notify(subject=subject, message=message)
