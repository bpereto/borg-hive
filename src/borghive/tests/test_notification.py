import datetime

import unittest
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from borghive.models import Repository, EmailNotification

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

    def test_update_invalid_alertpref(self):
        data = {
            'alert-pref': '',
            'alert_interval': '200',
            'alert_expiration': '9999'
        }
        response = self.client.post(reverse('notification-list'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(username='admin').alertpreference.alert_interval, 12)
        self.assertEqual(User.objects.get(username='admin').alertpreference.alert_expiration, 5)


class EmailNotificationTest(TestCase):

    fixtures = [
        'testing/users.yaml'
    ]

    def test_send_email_notification(self):
        notification = EmailNotification.objects.create(email='hohoho@northpole.local', owner=User.objects.get(username='admin'))
        notification.notify('test subject', 'test message')
