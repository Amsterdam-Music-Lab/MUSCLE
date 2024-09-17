# Start the application

## Before installation
We recommend downloading a code editor, for instance [Visual Studio Code](https://code.visualstudio.com/), and to use [git](https://git-scm.com/) to copy this repository to your machine, as this makes it easier to keep your local copy up to date.

## Installation with Docker
The easiest way to run the application locally is through Docker or Podman. Docker is an application which runs a network of virtual machines ("containers") and is therefore (mostly) platform independent.

The benefits of using Podman is that it is open source and can easily be used without root access. When using Podman with scripts in this documentation, `docker` and `docker-compose` should be replaced with `podman` and `podman-compose`. Alternatively, Docker could be aliased to Podman (`alias docker=podman` and `alias docker-compose=podman-compose`).

### Mac OS X or Windows 10
Install [Docker Desktop](https://docs.docker.com/desktop/).

### Linux
* Install [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/), or [Docker Desktop](https://docs.docker.com/desktop/).
* To install [Podman](https://podman.io/) on Debian-based distributions, install packages `podman` and `podman-compose`.

## Development server
Make a copy of the file .env.dist (in the same directory as this README) and rename it to .env. This file contains variables used by Docker to start up a container network serving MUSCLE.

Start Docker (the app icon is a whale carrying containers). Then, open a terminal and run
`docker-compose up` (add `sudo` on Linux).
This command starts up the containers defined in `docker-compose.yaml`:
- a PostgreSQL container, for storing experiment/user/playlist data, saved on the host machine in the Docker user data, represented in the volume `db_data`. Data added to the database will persist if the container is shut down.
- a ip2country container, which provides country codes for ip addresses, used for demographic information of users.
- a container of the server, defined in DockerfileDevelop in `backend`. The Dockerfile defines the Python version and installs development dependencies. The startup command runs migrations, adds a superuser (as defined in the `.env` file), playlist and basic experiment and then starts up a Django development server.
- a container of the client, defined in DockerfileDevelop in `frontend`. The Dockerfile defines the node version and installs node modules. The startup command kicks off a React development server.

## Navigate to the admin and user interface

Once you see all containers have started up, open your browser and navigate to [http://localhost:3000](http://localhost:3000). You should now be able to see the first screen of the Goldsmiths Musical Sophistication Index questionnaire.

To see the admin interface, navigate to [http://localhost:8000/admin](http://localhost:8000/admin).

Since the `docker-compose.yaml` defines bind mounts for `backend` and `frontend`, any changes to the files on the host are immediately reflected in the containers, which means code watching works and hot reload works in the same way as with a native node or Django server.

To stop the containers, press `ctrl-c` or (in another terminal) run
`docker-compose down`.

## Production build
A production build should define its own `docker-compose.yaml`, making use of the `Dockerfile` of the `backend` and `frontend` environments. It should also define a custom .env file, with safe passwords for the SQL database and the Python backend. Instead of mounting the entire backend and frontend directory and using the development servers, the backend should serve with gunicorn, and the frontend should use a build script to compile static html, css and JavaScript.

## Updating the application

The MUSCLE platform is in continuous development and new features and bug fixes are added to the codebase on a daily basis. To update the platform, checkout the `main` branch (which is contains the latest stable release) or the `develop` branch (which contains new not yet released features), pull the latest changes using `git pull`, and rebuild the docker containers using `docker-compose up --build`. Additionally, before rebuilding the containers, you might want to check if new or updated environment variables should be updated by comparing your `.env` file with the `.env.dist` file, which contains the environment variables that can or should be used.

### In short:

```sh
# 1. Checkout the main or develop branch
git checkout main # or git checkout develop

# 2. Pull the latest features, bug fixes, and other changes.
git pull

# 3. Compare your .env file with the .env.dist file and update your environment variables accordingly
diff -y .env .env.dist # This command (available on Linux & macOS) might help you with that

# 4. Rebuild & restart the containers
docker compose up --build
```
