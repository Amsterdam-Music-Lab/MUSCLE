# AML Experiment application
This application is a combination of the Hooked server and Hooked client of the Amsterdam Music Lab, generalized for use in a wide variety of experiments.

## Install Docker
To run the application locally, you will need to install Docker.

### Mac OS X or Windows 10
Install [Docker Desktop](https://docs.docker.com/desktop/).

### Linux
* Install [Docker Engine](https://docs.docker.com/engine/install/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)

As of April 2022, [Docker Desktop for Linux](https://docs.docker.com/desktop/linux/) is still in Beta and have not been tested by us.

## Development build
Make a file called .env next in this directory, with the following settings. Change database name and user and passwords as appropriate. The only setting that you'll have to set later is the slug, which depends on the slug (short name) of an existing experiment in your database.
```
SQL_DATABASE=aml
SQL_USER=aml
SQL_PASSWORD=supersecretpassword
SQL_HOST=db
SQL_PORT=5432

AML_SECRET_KEY=secretdjangopassword
AML_LOCATION_PROVIDER=http://ip2country:5000/{}
AML_DEBUG=True
DJANGO_SETTINGS_MODULE=aml.development_settings

REACT_APP_API_ROOT=http://localhost:8000
REACT_APP_EXPERIMENT_SLUG=your_slug
REACT_APP_AML_HOME=https://www.amsterdammusiclab.nl
```
Then, open a console and run
`docker-compose up` (add `sudo` on Linux).
This command makes use of the `docker-compose.yaml`, which defines four containers:
- a PostgreSQL container, for storing experiment/user/playlist data, saved on the host machine in the Docker user data, represented in the volume `db_data`. Data added to the database will persist if the container is shut down.
- a ip2country container, which provides country codes for ip addresses. This container is mainly interesting for running tests during development.
- a container of the server, defined in DockerfileDevelop in `backend`. The Dockerfile defines the Python version and installs development dependencies. The startup command runs migrations and then starts up a Django development server.
- a container of the client, defined in DockerfileDevelop in `frontend`. The Dockerfile defines the node version and installs node modules. The startup command kicks off a React development server.

Since the `docker-compose.yaml` defines bind mounts for `backend` and `frontend`, any changes to the files on the host are immediately reflected in the containers, which means code watching works and hot reload works in the same way as with a native node or Django server.

To stop the containers, press `ctrl-c` or (in another console) run
`docker-compose down`.

### Creating experiments and playlists
The admin interface is accessible at `localhost:8000/admin`. Before logging in, create a superuser by logging into the container of the backend. To find out the name, run `docker ps`, it should list all running container names. The container of the backend is most likely called `aml-experiments_server_1` (check 'NAMES' column). To connect to it, run:
`docker exec -it aml-experiments_server_1 bash`
This lets you execute shell commands on the container.
Then run `./manage.py createsuperuser`, and proceed to enter username, password and email address as prompted. After that, you can log into the admin interface to create a playlist and experiment. Make sure to adjust `REACT_APP_EXPERIMENT_SLUG` in your .env file accordingly.

### Compiling a playlist and other management commands
You can run management commands, such as dump the database or compile the playlist, by using the management container, as specified in `docker-compose-manage.yaml`.

For instance, to compile a playlist:
`docker-compose -f docker-compose-manage.yaml run manage ./manage.py compileplaylist path_to_sound_folder`

Other important management commands:
- Export experiment data to json: `./manage.py exportexperiment your_slug`
- Export how often sections have been played: `./manage.py exportplaycount playlist_id`
- Update translation strings in .po file: `./manage.py makemessages -l nl` or `./manage.py makemessages --all`
- Compile translations into binary .mo file: `./manage.py compilemessages`

### Debugging
If all containers are running via docker-compose, it is not possible to interact with the debug shell. Therefore, you need to do the following:
`docker ps` to list all running containers
`docker rm -f name_of_server_container`
`docker-compose run --rm --service-ports server`
After that, if you place a `breakpoint()` anywhere in the code, you can step through and inspect values of variables.


## Production build
A production build should define its own `docker-compose.yaml`, making use of the `Dockerfile` of the `backend` and `frontend` environments. Instead of mounting the entire backend and frontend directory and using the development servers, the backend should serve with gunicorn, and the frontend should build its files. An example of this setup can be found in the aml-deployment repository.

Creating superusers or running management commands will work in essentially the same way as documented above for the development setting.
