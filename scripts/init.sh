#!/usr/bin/env bash

cat << "EOF"
  ____                    _    _ _
 |  _ \                  | |  | (_)
 | |_) | ___  _ __ __ _  | |__| |___   _____
 |  _ < / _ \| '__/ _` | |  __  | \ \ / / _ \
 | |_) | (_) | | | (_| | | |  | | |\ V /  __/
 |____/ \___/|_|  \__, | |_|  |_|_| \_/ \___|
                   __/ |
                  |___/
EOF

DEBUG="${DEBUG:-True}"
MIGRATE="${MIGRATE:-True}"
FIXTURES="${FIXTURES:-True}"
BORGHIVE_ADMIN_USER="${BORGHIVE_ADMIN_USER:-admin}"

echo "DEBUG:     ${DEBUG}"
echo "MIGRATE:   ${MIGRATE}"
echo "FIXTURES:  ${FIXTURES}"
echo ""

#
# STATIC FILES
#
echo "Collect static files"
./manage.py collectstatic --noinput
echo ""

#
# DB INIT
#
if [[ ! -z "${MYSQL_DATABASE}" ]]; then
  echo -n "Waiting for database"

  until echo "select 1;" | ./manage.py dbshell > /dev/null
  do
    echo -n "."
    sleep 1
  done
  echo ""
  echo "DB started"
fi

#
# MIGRATE
#
if [[ "${MIGRATE}" == "True" ]]; then
  echo "Migrate..."
  ./manage.py migrate --no-input --force-color
  echo ""
fi

#
# CREATE SUPERUSER
#
if [[ ! -z "${BORGHIVE_ADMIN_PASSWORD}" ]]; then

  # create admin account if not exists
  SUPERUSER_EXISTS=$(echo "SELECT * from auth_user;" | ./manage.py dbshell | grep "${BORGHIVE_ADMIN_USER}")
  if [[ -z "${SUPERUSER_EXISTS}" ]]; then
    echo "Create superuser: ${BORGHIVE_ADMIN_USER}"
    cat <<EOD | ./manage.py shell
import os
from django.contrib.auth.models import User
User.objects.create_superuser(
  os.getenv('BORGHIVE_ADMIN_USER'),
  os.getenv('BORGHIVE_ADMIN_MAIL', 'root@localhost'),
  os.getenv('BORGHIVE_ADMIN_PASSWORD')
)
EOD
  else
    echo "Superuser \"${BORGHIVE_ADMIN_USER}\" exists already"
  fi

  # set superuser password
  echo "Set superuser password"
  cat <<EOD | ./manage.py shell
import os
from django.contrib.auth.models import User
u = User.objects.get(username=os.getenv('BORGHIVE_ADMIN_USER'))
u.set_password(os.getenv('BORGHIVE_ADMIN_PASSWORD'))
u.save()
EOD

echo ""
fi

#
# LOAD DATA
#
if [[ "${FIXTURES}" == "True" ]]; then
  echo "Load data / fixtures..."
  ./manage.py loaddata borghive/fixtures/setup/*
  echo ""
fi

#
# MODE
#
if [[ "${DEBUG}" == "True" ]]; then
  ./manage.py runserver 0.0.0.0:8000
else
  uwsgi --ini /uwsgi.ini --show-config
fi
