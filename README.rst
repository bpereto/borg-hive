What is Borg Hive?
------------------

Borg Hive is a management interface for borgbackup repositories.

The main goal of Borg Hive is to provide a easy management of borg repositories and ssh keys, also provide notifications if there is a stale backup. Optionally, it collects some events and statistics what's happening.

I backup my peripherals at home with borgbackup, which works nice on my servers, android phones, laptops, worktsations and so on.
To keep the overview over my backups and which device haven't done one in a while I decided to write a dashboard for it. The focus is for backups at home, but Borghive should also work in the cloud or in an enterprise.

.. warning:: **This is under active development. It's Alpha!**

Features
--------
* Repository Managment
* Repository Statistics
* SSH-Key Management
* Notifications of stale backups (E-Mail, Pushover)
* Partially Repository Events (should be improved)
* Basic Object Permissions (Owner & Group) of repositories, SSH-Keys and notifications

What it should also have in the Future / Todo
----------------------------------------------
* More notification types

  * GET/POST Webhooks
  * Other wanted notification types

* REST API (Django Rest Framework)
* Send Logs from borg client / borgmatic to API
* Backup Scheduling & Trigger with Ansible -> AWX/Tower Integration

.. start-badges

|doc| |build| |coverage|

.. |doc| image:: https://readthedocs.org/projects/borg-hive/badge/?version=latest
        :alt: Documentation
        :target: https://borg-hive.readthedocs.org/en/latest/

.. |build| image:: https://api.travis-ci.com/bpereto/borg-hive.svg?branch=master
        :alt: Build Status
        :target: https://travis-ci.com/bpereto/borg-hive

.. |coverage| image:: https://codecov.io/github/bpereto/borg-hive/coverage.svg?branch=master
        :alt: Test Coverage
        :target: https://codecov.io/github/bpereto/borg-hive?branch=master

.. end-badges
