import datetime

import unittest
from django.test import Client
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


import sshpubkeys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

from borghive.lib.keys import get_ssh_host_key_infos
from borghive.models import SSHPublicKey
from borghive.forms import SSHPublicKeyForm


class SSHPublicKeyTest(TestCase):
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

    def test_update_rsa_key(self):
        self.test_create_valid_rsa_key()

        data = {
            'name': 'ole-new',
            'public_key': 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDAfHetFCwshETzQ414TZkueJPGLL0IzL9beFeNMJ9UqptLQqQn0/GGfILsXsE0wg5J3B4GIO5iWE2hjEHaoUNUNZu6xU18yMrFm8MzjV6zQnubeMvG9x8CEal9/G+SmbMTpGhGjWkyVENlpcQx8OVzxkkYODKSBuQX8MiXSQ3/OTqUBSvywYIobmarfVg6CERldjfYwNI95tXSxieRaBU5w9f12X4nA6fdPAB4JXOxH8XsQVXMB5dx417PD0niPa5mVkdaJItVWIx2Z7gDdoor9nHamZY8dCfOTw8NDlF7CGe/m6J1GgokYIsNpolsmlhFyvd8IfqxXd2eJIYw+nc+UcDXp81j4E7o3T2IBD1adNE76LpEKfYW/01jRGSF0NOI1BJYP7xHz5UDVUMAsl4Sv0fbFnjJW3IPKgNFDIbdj/GRa/JnrtUa9eluzxV1bvIVOSdtsKbjmUl/MuOLl1xrRcyHjParx7hvwW8AqcwyjMkmOgRpHovPnnNNZJ1Lw8c= ole@oleeee'
        }
        response = self.client.post(reverse('key-update', kwargs={'pk': 1}), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SSHPublicKey.objects.count(), 1)

    def test_update_invalid_rsa_key(self):
        self.test_create_valid_rsa_key()

        key = SSHPublicKey.objects.first()
        key.public_key = 'ssh-rsa AAAB3NzaC1yc2EAAAADAQABAAABgQDAfHetFCwshETzQ414TZkueJPGLL0IzL9beFeNMJ9UqptLQqQn0/GGfILsXsE0wg5J3B4GIO5iWE2hjEHaoUNUNZu6xU18yMrFm8MzjV6zQnubeMvG9x8CEal9/G+SmbMTpGhGjWkyVENlpcQx8OVzxkkYODKSBuQX8MiXSQ3/OTqUBSvywYIobmarfVg6CERldjfYwNI95tXSxieRaBU5w9f12X4nA6fdPAB4JXOxH8XsQVXMB5dx417PD0niPa5mVkdaJItVWIx2Z7gDdoor9nHamZY8dCfOTw8NDlF7CGe/m6J1GgokYIsNpolsmlhFyvd8IfqxXd2eJIYw+nc+UcDXp81j4E7o3T2IBD1adNE76LpEKfYW/01jRGSF0NOI1BJYP7xHz5UDVUMAsl4Sv0fbFnjJW3IPKgNFDIbdj/GRa/JnrtUa9eluzxV1bvIVOSdtsKbjmUl/MuOLl1xrRcyHjParx7hvwW8AqcwyjMkmOgRpHo'
        with self.assertRaises(sshpubkeys.exceptions.MalformedDataError):
            key.save()

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


class SSHPrivateKey(TestCase):

    def generate_ssh_key(self):
        # generate private/public key pair
        key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
            key_size=2048)

        # get public key in OpenSSH format
        public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
            serialization.PublicFormat.OpenSSH)

        # get private key in PEM container format
        private_key = key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        return private_key, public_key

    def setUp(self):
        settings.BORGHIVE['CONFIG_PATH'] = '/tmp'
        private_key, public_key = self.generate_ssh_key()
        with open('/tmp/ssh_host_rsa_key', 'w') as f:
            f.write(private_key.decode('utf-8'))
        with open('/tmp/ssh_host_rsa_key.pub', 'w') as f:
            f.write(public_key.decode('utf-8'))

    def test_get_ssh_host_key_infos(self):
        self.assertEqual(len(get_ssh_host_key_infos()), 1)
