.. _backup-chapter:

Backup Borg Hive
===========

LDAP
------------

If using the version with the openldap-backup container, 
the LDAP container backs up it's data via a cron job that can be configured
in your `.env` file:

.. code-block:: env

    LDAP_BACKUP_CONFIG_ENV="5 * * * *"
    LDAP_BACKUP_DATA_ENV="*/5 * * * *"

For a backup of the config every 5th minute past the hour, a data backup every 5 minutes.

Restoring an LDAP backup
-----

To restore an LDAP backup to an openldap container, run the following commands:

.. code-block:: bash

    docker exec -it openldap-backup bash
    sv stop /container/run/process/slapd
    rm -r /etc/ldap/slapd.d/*
    slapd-restore-config 20190502T082301-config
    sv stop /container/run/process/slapd
    rm /var/lib/ldap/* 
    slapd-restore-data 20190502T080901-data


MySQL/MariaDB
-------------

Find the IP of the MariaDB container:
:code:`sudo docker ps`
and look for the container ID of MariaDB .

:code:`sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <Docker Container ID>`

This will give you the IP of the MariaDB container.

To get a dump from this, you can use MySQLDump, with the -h flag:
:code:`mysqldump -h <IP of Container> -u <username> -p<password> borghive > /var/backup/mybackup.sql`

Note to replace the username, IP, password and possibly the database name (borghive) and the target file, with your own
configuration.

If you use Borgmatic to back up the Borg Hive, the MySQL/MariaDB config can be entered
in the YAML file of Borgmatic.
