import datetime

import unittest
import unittest.mock as mock
from unittest import skip

from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core import mail
from django.contrib.auth.models import User
from borghive.models import Repository, RepositoryUser, RepositoryEvent
from borghive.models import EmailNotification, PushoverNotification
from borghive.tasks import alert_guard_tour

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

    def test_post(self):
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
        self.assertEqual(len(mail.outbox), 1)


class PushoverNotificationTest(TestCase):

    fixtures = [
        'testing/users.yaml'
    ]

    @mock.patch('requests.post', autospec=True)
    def test_send_pushover_notification(self, monkey):
        notification = PushoverNotification.objects.create(name='spock an enterprise', user='abc', token='xyz', owner=User.objects.get(username='admin'))
        notification.notify('unittest')
        self.assertTrue(monkey.called)
        monkey.assert_called_with('https://api.pushover.net:443/1/messages.json', data={'user': 'abc', 'token': 'xyz', 'message': 'unittest'})


class AlertTest(TestCase):

    fixtures = [
        'testing/users.yaml',
    ]

    def test_alert_should_not_1d_23h(self):
        # after 1 day - 23 hours old : should not alert
        repo1 = Repository.objects.create(owner=User.objects.first(), repo_user=RepositoryUser.objects.create(), name='repo1', alert_after_days=1)
        repo1.last_updated = timezone.now() - datetime.timedelta(hours=23)

        firing, alert = repo1.should_alert()
        self.assertFalse(firing)
        self.assertFalse(alert)

    def test_alert_should_not_2d_25h(self):
        # after 2 days - 25 hours old : should not alert
        repo2 = Repository.objects.create(owner=User.objects.first(), repo_user=RepositoryUser.objects.create(), name='repo2', alert_after_days=2)
        repo2.last_updated = timezone.now() - datetime.timedelta(hours=25)

        firing, alert = repo2.should_alert()
        self.assertFalse(firing)
        self.assertFalse(alert)

    def test_alert_should_1d_25h(self):

        # after 1 day: should alert
        repo3 = Repository.objects.create(owner=User.objects.first(), repo_user=RepositoryUser.objects.create(), name='repo3', alert_after_days=1)
        repo3.last_updated = timezone.now() - datetime.timedelta(hours=25)

        firing, alert = repo3.should_alert()
        self.assertTrue(firing)
        self.assertTrue(alert)

    def test_alert_should_1d_24h(self):
        # after 1 days - 24 hours old : should alert
        repo4 = Repository.objects.create(owner=User.objects.first(), repo_user=RepositoryUser.objects.create(), name='repo4', alert_after_days=1)
        repo4.last_updated = timezone.now() - datetime.timedelta(hours=24)
        repo4.save()

        firing, alert = repo4.should_alert()
        self.assertTrue(firing)
        self.assertTrue(alert)

    def test_alert_should_notify(self):
        # after 1 days - 26 hours old : should alert and notify
        user = User.objects.first()
        repo5 = Repository.objects.create(owner=user, repo_user=RepositoryUser.objects.create(), name='repo5', alert_after_days=1)
        repo5.last_updated = timezone.now() - datetime.timedelta(hours=26)
        repo5.save()
        email = EmailNotification.objects.create(email='hohoho@northpole.local', owner=user)

        firing, alert = repo5.should_alert()
        self.assertTrue(firing)
        self.assertTrue(alert)

        self.assertEqual(len(mail.outbox), 0)

        self.assertTrue(repo5.alert())

        alert_event = repo5.repositoryevent_set.last()
        self.assertEqual(alert_event.event_type, RepositoryEvent.ALERT)
        self.assertEqual(alert_event.message, 'Last backup of repo5 is older than 1 days')

        self.assertEqual(len(mail.outbox), 1)

    def test_alert_guard_tour(self):
        user = User.objects.first()
        repo6 = Repository.objects.create(owner=user, repo_user=RepositoryUser.objects.create(), name='repo6', alert_after_days=1)
        repo6.last_updated = timezone.now() - datetime.timedelta(hours=26)
        repo6.save()
        email = EmailNotification.objects.create(email='eltorroloco@burrito.local', owner=user)

        alert_guard_tour()
        self.assertEqual(len(mail.outbox), 1)

    def test_alert_interval(self):
        user = User.objects.first()
        repo7 = Repository.objects.create(owner=user, repo_user=RepositoryUser.objects.create(), name='repo7', alert_after_days=1)
        repo7.last_updated = timezone.now() - datetime.timedelta(hours=26)
        repo7.save()
        email = EmailNotification.objects.create(email='eltorroloco@burrito.local', owner=user)

        alert_guard_tour(repo_id=repo7.id)
        self.assertEqual(len(mail.outbox), 1)
        alert_guard_tour(repo_id=repo7.id)
        self.assertEqual(len(mail.outbox), 1)

        # backdate last alert event
        last_alert = repo7.repositoryevent_set.filter(
            event_type=RepositoryEvent.ALERT).last()
        last_alert.created -= datetime.timedelta(hours=12)
        last_alert.save()

        alert_guard_tour(repo_id=repo7.id)
        self.assertEqual(len(mail.outbox), 2)

    def test_alert_expiration(self):
        user = User.objects.first()
        repo8 = Repository.objects.create(owner=user, repo_user=RepositoryUser.objects.create(), name='repo8', alert_after_days=1)
        repo8.last_updated = timezone.now() - datetime.timedelta(days=7)
        repo8.save()
        email = EmailNotification.objects.create(email='eltorroloco@burrito.local', owner=user)

        alert_guard_tour(repo_id=repo8.id)
        self.assertEqual(len(mail.outbox), 1)

        # backdate last alert event
        last_alert = repo8.repositoryevent_set.filter(
            event_type=RepositoryEvent.ALERT).last()
        last_alert.created -= datetime.timedelta(days=6)
        last_alert.save()

        alert_guard_tour(repo_id=repo8.id)
        self.assertEqual(len(mail.outbox), 1)
