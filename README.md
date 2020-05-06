# Borg Hive

Borg Hive - a Borgbackup Server Interface

**This is under active development. It's Alpha State!**

I backup my peripherals at home with borgbackup, which works nice on my servers, android phones, laptops, worktsations and so on.   
To keep the overview over my backups and which device haven't done one in a while I decided to write a dashboard for it. The focus is for backups at home, but Borghive should also work in the cloud.

## Get started
```
docker-compose up
docker exec -it borg-hive_app_1 /bin/bash
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata fixtures/*
```
