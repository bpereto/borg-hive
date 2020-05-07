import datetime

import unittest
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from borghive.models import SSHPublicKey

from borghive.forms import SSHPublicKeyCreateForm


class SSHPublicKeyCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])

    def test_get(self):
        response = self.client.get(reverse('key-create'))
        self.assertEqual(response.status_code, 200)

    def test_create_valid_rsa_key(self):
        data = {
            'name': 'ole',
            'public_key': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDAfHetFCwshETzQ414TZkueJPGLL0IzL9beFeNMJ9UqptLQqQn0/GGfILsXsE0wg5J3B4GIO5iWE2hjEHaoUNUNZu6xU18yMrFm8MzjV6zQnubeMvG9x8CEal9/G+SmbMTpGhGjWkyVENlpcQx8OVzxkkYODKSBuQX8MiXSQ3/OTqUBSvywYIobmarfVg6CERldjfYwNI95tXSxieRaBU5w9f12X4nA6fdPAB4JXOxH8XsQVXMB5dx417PD0niPa5mVkdaJItVWIx2Z7gDdoor9nHamZY8dCfOTw8NDlF7CGe/m6J1GgokYIsNpolsmlhFyvd8IfqxXd2eJIYw+nc+UcDXp81j4E7o3T2IBD1adNE76LpEKfYW/01jRGSF0NOI1BJYP7xHz5UDVUMAsl4Sv0fbFnjJW3IPKgNFDIbdj/GRa/JnrtUa9eluzxV1bvIVOSdtsKbjmUl/MuOLl1xrRcyHjParx7hvwW8AqcwyjMkmOgRpHovPnnNNZJ1Lw8c= ole@ole'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SSHPublicKey.objects.count(), 1)

    def test_create_valid_ed25519_key(self):
        data = {
            'name': 'key-ed25519',
            'public_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJy2GMJLrWk7AiHWRA8crkfxcbqGfx8mCR4/ox3C9pZe ole@ole'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SSHPublicKey.objects.count(), 1)

    def test_create_valid_ecdsa_key(self):
        data = {
            'name': 'key-ecdsa',
            'public_key': 'ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOltDNue+Pa939EWFoTJAEAbXfrD92mVsVut8TQZh4/zyQEOP5M2bK+KFbEKal9lALiGLIJbz/7tS13Td6KYqrA= ole@ole'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SSHPublicKey.objects.count(), 1)

    def test_create_valid_key_newline(self):
        data = {
            'name': 'key-ed25519-xxx',
            'public_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJy2GMJLrWk7AiHWRA8crkfxcbqGfx8mCR4/ox3C9pZe asdf@asdf\n'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(SSHPublicKey.objects.count(), 1)

    def test_create_invalid_key_without_comment(self):
        data = {
            'name': 'key-ed25519-x',
            'public_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJy2GMJLrWk7AiHWRA8crkfxcbqGfx8mCR4/ox3C9pZe'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(SSHPublicKey.objects.count(), 1)

    def test_create_invalid_key_commentspace(self):
        data = {
            'name': 'key-ed25519-xx',
            'public_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJy2GMJLrWk7AiHWRA8crkfxcbqGfx8mCR4/ox3C9pZe asdf@asdf asdf asdf'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(SSHPublicKey.objects.count(), 0)

    def test_invalid_key(self):
        data = {
            'name': 'key-ed25519-xxx',
            'public_key': 'ssh-ed25519 AAAC3NzaC1lZDI1NTE5AAAAIJy2GMJLr7AiHWRA8crkfxcbqGfx8mCR4/ox3C9pZe ole@ole'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(SSHPublicKey.objects.count(), 0)

    def test_invalid_key2(self):
        data = {
            'name': 'key-ed25519-xxxx',
            'public_key': 'ssh-ed25519 AAAAC3NzaC1lZD";"a\';>sdf ole@ole'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(SSHPublicKey.objects.count(), 0)

    def test_invalid_key3(self):
        data = {
            'name': 'key-asdf',
            'public_key': 'ssh-asdf AAAAC3xxxx'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(SSHPublicKey.objects.count(), 0)

    def test_invalid_key3(self):
        data = {
            'name': 'key-asdf',
            'public_key': 'ssh-rsa AAAAC3xölsdflkdf$$$$$@@@$$adx'
        }
        response = self.client.post(reverse('key-create'), data=data)
        self.assertEqual(SSHPublicKey.objects.count(), 0)
