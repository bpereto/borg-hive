import subprocess
import shutil

from celery.utils.log import get_task_logger

from borghive.models import Repository
from core.celery import app

LOGGER = get_task_logger(__name__)


@app.task
def create_repo_statistic(repo_id=None):
    """create repository statistic for one or multiple repos - async"""
    if repo_id:
        repos = Repository.objects.filter(id=repo_id)
    else:
        repos = Repository.objects.all()

    LOGGER.info('refresh repo statistics for: %s', repos)
    for repo in repos:
        repo.refresh()


@app.task
def get_repo_size(repo_id):
    """get repo size - heavy fs operation"""
    repo = Repository.objects.get(id=repo_id)
    return subprocess.check_output(['du', '-sm', repo.get_repo_path()]).split()[0].decode('utf-8')

@app.task
def repository_delete(repo_path):
    """delete repository on filesystem"""
    LOGGER.info('delete repository: %s', repo_path)
    try:
        shutil.rmtree(repo_path)
    except FileNotFoundError:
        LOGGER.warning('repository path does not exist: %s', repo_path)