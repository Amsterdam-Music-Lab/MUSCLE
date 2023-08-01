# MUSic-related Citizen Science Listening Experiments (MUSCLE)
This application provides an easy way to implement and run online listening experiments for music research. It presents questions, and typically audio stimuli, to participants, and collects their feedback.

## Try MUSCLE
- Try the already implemented experiments at the [Amsterdam Music Lab Website](https://www.amsterdammusiclab.nl/experiments/).

- For documentation on how to use the infrastructure, refer to our [wiki](https://github.com/Amsterdam-Music-Lab/aml-experiments/wiki).

- We are also happy if you file a feature request in our [issues list](https://github.com/Amsterdam-Music-Lab/aml-experiments/issues), or if you fork this repository to add your own code.

## Installation with Docker
The easiest way to run the application locally is through Docker.

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

## Production build
A production build should define its own `docker-compose.yaml`, making use of the `Dockerfile` of the `backend` and `frontend` environments. Instead of mounting the entire backend and frontend directory and using the development servers, the backend should serve with gunicorn, and the frontend should use a build script to compile static html, css and JavaScript.
