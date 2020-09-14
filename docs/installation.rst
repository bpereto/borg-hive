
Installation
============

The application is optimized for a containerized setup.

There are different ways to install and run Borg-Hive:

- :ref:`docker` - setup with docker and docker-compose
- :ref:`k8s` - easy and fast deployment with helm to kubernetes

.. _docker:

Docker
------

Prerequisites: You should have docker and docker-compose installed and running.

.. code-block:: bash

   # Configure the environment and optionally set EMAIL or LDAP settings
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

Open the browser and navigate to your host: ex. http://localhost:8000

.. _k8s:

Kubernetes
----------

Prerequisites:

- You should have setup your k8s and kubectl
- You installed helm
- You have an nginx ingress running (the charts must be adjusted to use other ingresses)

Configuration:

- Adjust the DNS-Name in :code:`values.yaml`
- Configure the DNS-Name in your DNS and point it to the Ingress-IP of k8s.

.. code-block:: bash

   # Add helm repo of bitnami
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm dep update

   # create own namespace in k8s for borg-hive
   kubectl create namespace borg-hive

   # mariadb should be installed first
   helm install mariadb bitnami/mariadb --namespace borg-hive -f values.db.yaml
   helm upgrade --install borg-hive . -f values.yaml --namespace borg-hive     

.. important:: :code:`helm upgrade` does regenerate the secrets (passwords) of mariadb and openldap.
                therefore the mariadb is installed sepparate. Keep in mind: on each helm upgrade, the pods of borg-hive should be deleted (and will be recreated) to adjust the secret for openldap in the container.

**Services**

- The web-tier should now be accessible through the ingress.
  In this example: https://borg-hive.app.local
- borgbackup should now be accessible through the Loadbalancer IP. In this example: 192.168.101.204:22

.. code-block:: bash

   # kubectl get services --namespace borg-hive       
    
   borg-hive-app        ClusterIP      10.111.108.79   <none>            8000/TCP          40h
   borg-hive-borg       LoadBalancer   10.100.163.89   192.168.101.204   22:30198/TCP      40h
   borg-hive-openldap   ClusterIP      10.97.223.166   <none>            389/TCP,636/TCP   38h
   mariadb              ClusterIP      10.97.32.101    <none>            3306/TCP          2d14h
   mariadb-slave        ClusterIP      10.96.86.61     <none>            3306/TCP          2d14h
   redis-headless       ClusterIP      None            <none>            6379/TCP          39h
   redis-master         ClusterIP      10.97.123.94    <none>            6379/TCP          39h
   redis-slave          ClusterIP      10.96.114.224   <none>            6379/TCP          39h

