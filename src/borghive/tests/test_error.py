from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from borghive.views.error import error404,error403,error500

from core.celery import debug


class ErrorPageTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_404(self):
        request = self.factory.get('/')
        response = error404(request)
        self.assertEqual(response.status_code, 404)
    
    def test_403(self):
        request = self.factory.get('/')
        response = error403(request)
        self.assertEqual(response.status_code, 403)

    def test_500(self):
        request = self.factory.get('/')
        response = error500(request)
        self.assertEqual(response.status_code, 500)