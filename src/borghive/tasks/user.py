import os
import subprocess

from celery.utils.log import get_task_logger
from django.conf import settings

from borghive.models import RepositoryUser
from core.celery import app

LOGGER = get_task_logger(__name__)


@app.task
def generate_login_config():
    PASSWD = \
'''root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
borg:x:1000:1000:Borghive User:/home/borg:/bin/bash
'''
    SHADOW = \
'''root:*:18374:0:99999:7:::
daemon:*:18374:0:99999:7:::
bin:*:18374:0:99999:7:::
sys:*:18374:0:99999:7:::
man:*:18374:0:99999:7:::
nobody:*:18374:0:99999:7:::
sshd:*:18384:0:99999:7:::
borg:*:18384:0:99999:7:::
'''

    PASSWD_LINE_PATTERN = '{}:x:{}:{}:Borghive Repository User:{}:/bin/bash\n'
    SHADOW_LINE_PATTERN = '{}:*:18384:0:99999:7:::\n'

    for user in RepositoryUser.objects.all(): # filter(repository__isnull=False):
        LOGGER.debug(user)
        # @TODO: homepath from settings
        PASSWD += user.get_passwd_line()
        SHADOW += user.get_shadow_line()

    print(PASSWD.strip())
    print(SHADOW.strip())
    LOGGER.debug(PASSWD)
    LOGGER.debug(SHADOW)

    with open(os.path.join(settings.BORGHIVE['LOGIN_CONFIG_PATH'], 'passwd'), 'w') as f_passwd:
        f_passwd.write(PASSWD)
    with open(os.path.join(settings.BORGHIVE['LOGIN_CONFIG_PATH'], 'shadow'), 'w') as f_shadow:
        f_shadow.write(SHADOW)


@app.task
def create_repo_user(user_id):
    user = RepositoryUser.objects.get(id=user_id)
    with open(os.path.join(settings.BORGHIVE['LOGIN_CONFIG_PATH'], 'passwd'), 'a') as f_passwd:
        f_passwd.write(user.get_passwd_line())
    with open(os.path.join(settings.BORGHIVE['LOGIN_CONFIG_PATH'], 'shadow'), 'a') as f_shadow:
        f_shadow.write(user.get_shadow_line())
