from django.test import TestCase
from borghive.templatetags.helpers import humanmegabytes


class LibTest(TestCase):
    """test lib functions"""

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
