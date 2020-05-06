import os
from core.celery import app
from borghive.models import RepositoryUser, Repository
from django.conf import settings

from celery.utils.log import get_task_logger

LOGGER = get_task_logger(__name__)

import subprocess

@app.task
def create_repo_statistic(repo_id=None):
    if repo_id:
        repos = Repository.objects.filter(id=repo_id)
    else:
        repos = Repository.objects.all()

    LOGGER.info('refresh repo statistics for: {}'.format(repos))
    for repo in repos:
        repo.refresh()

@app.task
def get_repo_size(repo_id):
    repo = Repository.objects.get(id=repo_id)
    return subprocess.check_output(['du','-sm', repo.get_repo_path()]).split()[0].decode('utf-8')
