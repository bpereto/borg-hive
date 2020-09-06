.. borg-hive documentation master file, created by
   sphinx-quickstart on Wed May  6 23:27:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Quick Start
===========

This chapter will get you started with Borg Hive.

Get started
-------------
For development Setup look into :ref:`Development`

Prerequisites: You should have Docker installed and Running.

.. code-block:: bash

   # Configure the Environment, set EMAIL or LDAP Settings
   vi .env

   # start app
   docker-compose up

   # wait untill both the db worker complete initialization
   # and "waiting for connections", restart the app
   docker-compose down; docker-compose up

   # wait untill the app worker is finished setting up

   # change into app container
   docker exec -it borg-hive_app_1 /bin/bash

   # create superuser
   ./manage.py createsuperuser

Open the browser and navigate to your host: ex. http://localhost:80

-----------------------------------------------------------------------------

.. image:: img/borghive-overview.png
