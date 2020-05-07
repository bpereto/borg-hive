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

echo "DEBUG:     ${DEBUG}"
echo "MIGRATE:   ${MIGRATE}"
echo "FIXTURES:  ${FIXTURES}"


#
# STATIC FILES
#
./manage.py collectstatic --noinput

#
# DB INIT
#
if [[ -z "$MYSQL_DATABASE" ]];
then
    echo "Waiting for database..."

    while ! nc -z db 3306; do
      sleep 1
    done

    echo "DB started"
fi

#
# MIGRATE
#
if [[ "${MIGRATE}" == "True" ]]; then
  ./manage.py migrate --no-input --force-color
fi

#
# LOAD DATA
#
if [[ "${FIXTURES}" == "True" ]]; then
  ./manage.py loaddata borghive/fixtures/setup/*
fi

#
# MODE
#
if [[ "${DEBUG}" == "True" ]]; then
  ./manage.py runserver 0.0.0.0:8000
else
  uwsgi --ini /uwsgi.ini --show-config
fi
