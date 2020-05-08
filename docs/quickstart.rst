.. borg-hive documentation master file, created by
   sphinx-quickstart on Wed May  6 23:27:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Quick Start
===========

This chapter will get you started with Borg Hive.

Get started
-------------
For development Setup look into :ref:development

Prerequisites: You should have Docker installed and Running.

.. code-block:: bash

   # start app
   docker-compose up

   # change into app container
   docker exec -it borg-hive_app_1 /bin/bash

   # create superuser
   ./manage.py createsuperuser


-----------------------------------------------------------------------------

.. image:: img/borghive-overview.png
