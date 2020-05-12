import os
from django.conf import settings
import ldapdb.models
from ldapdb.models import fields


class RepositoryLdapUser(ldapdb.models.Model):
    """
    Class for representing a repository user in LDAP
    """

    # pylint: disable=W0222

    # LDAP meta-data
    base_dn = settings.BORGHIVE['LDAP_USER_BASEDN']
    object_classes = ['organizationalPerson', 'posixAccount', 'shadowAccount']

    last_modified = fields.DateTimeField(db_column='modifyTimestamp')

    # posixAccount
    uid = fields.IntegerField(db_column='uidNumber', unique=True)
    group = fields.IntegerField(db_column='gidNumber')
    gecos = fields.CharField(db_column='gecos', default='Borghive Repo User')
    home = fields.CharField(db_column='homeDirectory', default=settings.BORGHIVE['REPO_PATH'])
    shell = fields.CharField(db_column='loginShell', default='/bin/bash')
    username = fields.CharField(db_column='uid', primary_key=True)
    sn = fields.CharField(db_column='sn', default='')
    cn = fields.CharField(db_column='cn', default='')

    def save(self, *args, **kwargs):
        self.home = os.path.join(settings.BORGHIVE['REPO_PATH'], self.username)
        self.sn = self.username
        self.cn = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return 'RepositoryLdapUser: {0.dn}: uid={0.uid} gid={0.group}'.format(self)
