import os
from core.celery import app
from borghive.models import RepositoryUser
from django.conf import settings

from celery.utils.log import get_task_logger

LOGGER = get_task_logger(__name__)

import subprocess

@app.task
def create_repo_statistic():

@app.task
def get_repo_size(repo_id):
    repo = Repository.objects.get(id=repo_id)
    return subprocess.check_output(['du','-sm', repo.get_repo_path()]).split()[0].decode('utf-8')
