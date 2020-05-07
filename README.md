# Borg Hive

Borg Hive - manage borgbackups

**This is under active development. It's Alpha State!**

I backup my peripherals at home with borgbackup, which works nice on my servers, android phones, laptops, worktsations and so on.   
To keep the overview over my backups and which device haven't done one in a while I decided to write a dashboard for it. The focus is for backups at home, but Borghive should also work in the cloud.

## Features
* Repository Managment
* Repository Statistics
* SSH-Key Management
* Notifications of stale backups
* Partially Repository Events

## What it should also have in the Future / Todo
* More Notification Types
  * GET/POST Webhooks
  * Pushover
  * https://github.com/jazzband/django-push-notifications
* REST API (Django Rest Framework)
* Better Documentation
* CI
* Container Image Generation


## Get started
```
docker-compose up
docker exec -it borg-hive_app_1 /bin/bash
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata fixtures/*
```
