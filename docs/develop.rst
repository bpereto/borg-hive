
.. _development-chapter:

Development
------------

Setup the development docker containers:

.. code-block:: bash

   docker-compose -f docker-compose.dev.yml up
   docker exec -it borg-hive_app_1 /bin/bash
   ./manage.py createsuperuser

Open the browser and navigate to your host: ex. http://localhost:8000
