
.. _development-chapter:

Development
------------

Setup the development docker containers.

The Database needs time to initialize the first time:

.. code-block:: bash

   docker-compose -f docker-compose.dev.yml up -d db
   docker-compose -f docker-compose.dev.yml up -d
   docker exec -it borg-hive_app_1 /bin/bash
   ./manage.py createsuperuser

Open the browser and navigate to your host: ex. http://localhost:8000
