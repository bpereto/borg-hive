from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User


from core.celery import debug

class ErrorPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get_or_create(username='admin')[0])

    def test_404(self):
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
