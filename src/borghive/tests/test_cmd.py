import datetime
import unittest
from io import StringIO
import sys
import os

from django.test import TestCase

from django.core import management


class CommandTest(TestCase):

    fixtures = [
        'testing/users.yaml',
        'testing/sshpubkeys.yaml',
        'testing/repositoryusers.yaml',
        'testing/repositories.yaml'
    ]

    def test_run_authorized_keys_check(self):
        out = StringIO()
        sys.stdout = out
        management.call_command("authorized_keys_check", "--user", "mhw349xu", stdout=out)
        num_keys = out.getvalue().count('\n')
        self.assertEqual(num_keys, 2)

    def test_run_authorized_keys_check(self):
        out = StringIO()
        sys.stdout = out
        os.environ['DEBUG'] = '0'
        # management.call_command("watch_repositories", "--repo-path", ".", stdout=out)  # @TODO: blocking command
