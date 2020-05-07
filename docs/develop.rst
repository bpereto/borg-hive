

Development
------------

Setup the Development Docker Containers:

.. code-block:: bash

   docker-compose -f docker-compose.dev.yml up
   docker exec -it borg-hive_app_1 /bin/bash
   ./manage.py createsuperuser
