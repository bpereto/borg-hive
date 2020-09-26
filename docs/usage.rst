
######
Usage
######

Documentation to the usage of Borg-Hive.


Import or Export existing Repositories
****************************************

If you already have an existing Borg repository you can import the archive into Borg-Hive with rsync. An export of the Borg repository is also possible in the same way.

.. note:: Due the nature of rsync it's possible to store arbitrary data besides a Borg repository in Borg-Hive, which is not recommended.

There are different repository modes to control the behaviour of the repository in borg-hive:

* **BORG**: (default) enables borgbackup operations
* **IMPORT**: enables write-only to the given repository location with rsync
* **EXPORT**: enables read-only to the given repository location with rsync

Only one mode can be active. It's not possible to import with rsync and do brogbackups at the same time.

Import existing Borg repository
--------------------------------

Create a new repository. Afterwards edit the repository and set the repository mode to :code:`IMPORT`.

Execute rsync to transfer the data to borg-hive:

.. code-block:: bash

    $ rsync -Paz --stats REPO-TO-IMPORT/ xxxxxx@borg-hive-app.local:

.. note:: The :code:`/` is required to copy the content of the folder and not the folder itself.

.. warning:: An import can also be executed on an existing repository, but be aware that the stored data will be overwritten or deleted.


Export existing Borg repository
--------------------------------

Edit the repository and set the repository mode to :code:`EXPORT`.

Execute rsync to transfer the data from borg-hive:

.. code-block:: bash

    $ rsync -Paz --stats xxxxxx@borg-hive-app.local: /home/my-local-repo
