from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class APIRepositoryTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(User.objects.get_or_create(username='admin')[0])

    def test_api_repository_list(self):

        self.test_api_repository_create()

        response = self.client.get(reverse('api:repository-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['name'], 'testrepo')

    def test_api_repository_create(self):
        data = {
            'name': 'testrepo',
            'ssh_keys': '2',
            'location_id': '1'
        }
        response = self.client.post(reverse('api:repository-list'), data=data)
        self.assertEqual(response.status_code, 201)
        return response.json()

    def test_api_repository_update(self):
        repository = self.test_api_repository_create()
        response = self.client.patch(repository['_href'], data={'alert_after_days': 3})
        self.assertEqual(response.status_code, 200)

    def test_api_repository_delete(self):
        repository = self.test_api_repository_create()

        response = self.client.delete(repository['_href'])
        self.assertEqual(response.status_code, 204)
