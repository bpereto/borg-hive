import datetime

import unittest
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from borghive.models import Repository

from borghive.forms import AlertPreferenceForm


class AlertPrefernceTest(TestCase):

    fixtures = [
        'testing/users.yaml',
    ]

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get_or_create(username='admin')[0])

    def test_get(self):
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, 200)

    def test_init_alertform(self):
        form = AlertPreferenceForm()

    def test_update_alertpref(self):
        data = {
            'alert-pref': '',
            'alert_interval': '13',
            'alert_expiration': '30'
        }
        response = self.client.post(reverse('notification-list'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(username='admin').alertpreference.alert_interval, 13)
        self.assertEqual(User.objects.get(username='admin').alertpreference.alert_expiration, 30)
