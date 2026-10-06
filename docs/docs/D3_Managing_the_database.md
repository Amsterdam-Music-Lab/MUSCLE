# Managing the database

The Docker infrastructure runs a PostgreSQL container. We can create backups of the database within this container, as well as restore the database.

This is especially useful in the following situations:
- before complex (data) migrations of the Django backend.
- before upgrading the PostgreSQL version

## Backup the PostgreSQL database

Run the following command from the top directory to back up the database:

`scripts/db-dump {optional-filename}`

In production, use the flag `-p` to make sure the correct `docker-compose` file is used for the environment variables, volumes, etc.

The backups are stored on the docker volume `db_backup` which mirrors `/backups` from the Postgresql container. If you do not provide a filename, the file will be named by the current date: `yyyymmdd.sql`.

## Restore the PostgreSQL database

In case you want to upgrade the PostgreSQL version, switch to a branch with the new version before restoring the database.

Run the following command from the top directory to restore the database:

`scripts/db-restore`

In production, use the flag `-p` to make sure the correct `docker-compose` file is used for the environment variables, volumes, etc.

The script will:
- stop and remove all running containers
- remove the contents of the `db_data` volume
- restart containers
- prompt you to select which files to restore (e.g., type `1` and hit enter to restore the first file in the list)
- restore the database and then restart all containers

NB: the files created via this script will always end in `sql`, whereas automatically created backups through GitHub actions will always end in `dump`. Both files can be used for restoring, but the `sql` file will be the most recent, so choose this one to prevent data loss.
