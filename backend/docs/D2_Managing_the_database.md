# Managing the database

The Docker infrastructure runs a PostgreSQL container. We can create backups of the database within this container, as well as restore the database.

### Backup the PostgreSQL database
Run the following command in the console to back up the database:

`docker-compose run --rm db bash -c "pg_dump aml -Fc > /backups/<filename>.dump"`

Use this command to make daily backups, numbered by the day of the month:

`docker-compose run --rm db bash -c "pg_dump aml -Fc > /backups/backup-$(date +"%d").dump"`

The backups are stored on the docker volume `db_backup` which mirrors `/backups` from the Postgresql container.

### Restore the postgreSQL database

Always stop the backend container first:

`docker stop aml-experiments_server_1`

Then drop, create and restore the database:

`docker-compose run --rm db bash -c "dropdb aml"`

`docker-compose run --rm db bash -c "createdb aml"`

`docker-compose run --rm db bash -c "pg_restore -d aml /backups/<filename>.dump"`

Restart the backend container: (or alternatively rebuilt the containers as descibed above) 

`docker start aml-experiments_server_1`

[>Next](https://github.com/Amsterdam-Music-Lab/aml-experiments/wiki/6.-Debugging)
