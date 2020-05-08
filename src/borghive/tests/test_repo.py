import datetime

import unittest
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

import borghive.exceptions
from borghive.models import Repository
from borghive.forms import RepositoryCreateForm


class RepositoryCreateTest(TestCase):

    fixtures = [
        'testing/users.yaml',
        'testing/sshpubkeys.yaml'
    ]
    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get_or_create(username='admin')[0])

    def test_get(self):
        response = self.client.get(reverse('repository-create'))
        self.assertEqual(response.status_code, 200)

    def test_create_repo(self):
        data = {
            'name': 'testrepo',
            'ssh_keys': '2'
        }
        response = self.client.post(reverse('repository-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Repository.objects.count(), 1)

    def test_injection(self):
        data = {
            'name': 'asdf"asd\'l\'\""fk',
            'ssh_keys': '2'
        }
        response = self.client.post(reverse('repository-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Repository.objects.count(), 0)

    def test_create_crazy_repo(self):
        data = {
            'name': '$6ç342lA/%=075akse!!½%#@',
            'ssh_keys': '2'
        }
        response = self.client.post(reverse('repository-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Repository.objects.count(), 0)


class RepositoryTest(TestCase):

    fixtures = [
        'testing/users.yaml',
        'testing/sshpubkeys.yaml',
        'testing/repositoryusers.yaml',
        'testing/repositories.yaml',
    ]

    def test_refresh(self):

        repo = Repository.objects.first()
        with self.assertRaises(borghive.exceptions.RepositoryNotCreated):
            repo.refresh()
