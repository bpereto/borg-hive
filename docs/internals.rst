 .. borg-hive documentation master file, created by
   sphinx-quickstart on Wed May  6 23:27:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Internals
===========

Some detail informations about the internals of borg hive.

Repository User
----------------

A unique Repository User is generated per Repository to ensure that only one Repository can be accessed.

So the structure on the filesystem looks like this:
:code:`/repos/<repo user>/<repo name>`

On Repository User create, a corresponding entry in passwd and shadow is generated, that sshd allows a login for this user.
It's not optimal to write and handle the shadow and passwd files. A possible solution is to use a PAM-Module to query the users from the database, ldap or similar.

The PAM configuration creates the directories on first user login.

Repository Events
------------------
Due to Borg's design to distrust the server as little information as possible is emitted on the server part and therefore its not easy to obtain correct informations about the repository.

At the moment the following is detected:

  * Borg Repository open: :code:`lock.exclusive` is created
  * Borg Repository close: :code:`lock.exclusive` is removed
  * Last Access: Modification Time of repository directory (because of create/delete of the lock file)
  * Last Update: Modification Time of the index.* files.
  * Backup Usage: Usage on Filesystem (du)

A future enhancement could be a plugin to `borgmatic <https://torsion.org/borgmatic/docs/how-to/monitor-your-backups>`_ to submit the information and logs via API to Borg Hive.

The management command :code:`watch_repositories` runs inotify on the repository directory and a combination of files and paths results in repository events.

Repository Statistic
--------------------

The Repository Statistic is obtained each day, when a repsitory is refreshed and after a "Repository Updated" Event is emitted.

SSH Authentication
--------------------

To prevent managing the ssh keys in authorized keys files per repo user on the filesystem, the ssh-keys are retrieved from the database.
When the User logs in, the management command :code:`authorized_keys_check` is executed by the sshd-server trough the statement: :code:`AuthorizedKeysCommand`

.. code-block:: bash

  Match User *
    AuthorizedKeysCommand /app/manage.py authorized_keys_check --user %u
    AuthorizedKeysCommandUser borg

The command expects on stdout lines of the format of the authorized keys.

After SSH-Key authentication, the user must be allowed through PAM. To ensure this, the repository user must exist in the passwd and shadow file.
To eliminate the need of the passwd and shadow file, an alternative PAM module could be used to retrieve the users.
