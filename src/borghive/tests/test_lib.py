from django.test import TestCase
from borghive.templatetags.helpers import humanmegabytes
import borghive.lib.rules
from borghive.models import Repository


class LibTest(TestCase):
    """test lib functions"""

    fixtures = [
        'testing/users.yaml',
        'testing/sshpubkeys.yaml',
        'testing/repositoryusers.yaml',
        'testing/repositories.yaml',
    ]

    def test_humanmegabytes(self):
        ret = humanmegabytes('o')
        self.assertEqual(ret, 'o')

        ret = humanmegabytes(50)
        self.assertEqual(ret, '50.0 MB')

        ret = humanmegabytes(1000)
        self.assertEqual(ret, '1000.0 MB')

        ret = humanmegabytes(2000)
        self.assertEqual(ret, '1.95 GB')

        ret = humanmegabytes(111111)
        self.assertEqual(ret, '108.51 GB')

        ret = humanmegabytes(1111111)
        self.assertEqual(ret, '1.06 TB')

    def test_rules(self):

        # is_owner
        repo = Repository.objects.first()
        owner = repo.owner
        self.assertTrue(borghive.lib.rules.is_owner(owner, repo))

        # owned_by_group
        self.assertTrue(borghive.lib.rules.owned_by_group(owner, repo))