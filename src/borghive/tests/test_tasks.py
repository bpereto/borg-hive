from django.test import TestCase
from django.urls import reverse

from core.celery import debug

class CeleryTaskTest(TestCase):

    fixtures = [
        'testing/users.yaml',
        'testing/sshpubkeys.yaml',
        'testing/repositoryusers.yaml',
        'testing/repositories.yaml'
    ]

    def test_task_debug(self):
        debug()
