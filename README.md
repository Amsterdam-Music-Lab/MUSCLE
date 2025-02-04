[![DOI](https://zenodo.org/badge/418963353.svg)](https://zenodo.org/badge/latestdoi/418963353) ![CI Backend](https://github.com/Amsterdam-Music-Lab/MUSCLE/actions/workflows/ci-backend.yml/badge.svg) ![CI Frontend](https://github.com/Amsterdam-Music-Lab/MUSCLE/actions/workflows/ci-frontend.yml/badge.svg) ![Test](https://github.com/Amsterdam-Music-Lab/MUSCLE/actions/workflows/test.yml/badge.svg)
![Backend Code Coverage Percentage](https://raw.githubusercontent.com/Amsterdam-Music-Lab/MUSCLE/code-coverage-badges/backend/coverage-backend-badge.svg)
![Frontend Code Coverage Percentage](https://raw.githubusercontent.com/Amsterdam-Music-Lab/MUSCLE/code-coverage-badges/frontend/coverage-frontend-badge.svg)

# MUSic-related Citizen Science Listening Experiments (MUSCLE)
This application provides an easy way to implement and run online listening experiments for music research. It presents questions, and typically audio stimuli, to participants, and collects their feedback.

## Try MUSCLE
- Try the already implemented experiments at the [Amsterdam Music Lab Website](https://www.amsterdammusiclab.nl/experiments/).

- For documentation on how to use the infrastructure, refer to our [documentation](https://amsterdam-music-lab.github.io/MUSCLE/).

- We are also happy if you file a feature request in our [issues list](https://github.com/Amsterdam-Music-Lab/aml-experiments/issues), or if you fork this repository to add your own code.

- Check out our [releases page](https://github.com/Amsterdam-Music-Lab/MUSCLE/releases) for the latest updates and changes.

## Before installation
We recommend downloading a code editor, for instance [Visual Studio Code](https://code.visualstudio.com/), and to use [git](https://git-scm.com/) to copy this repository to your machine, as this makes it easier to keep your local copy up to date.

## Installation with Docker
The easiest way to run the application locally is through Docker. Docker is an application which runs a network of virtual machines ("containers") and is therefore (mostly) platform independent.

### Mac OS X or Windows 10
Install [Docker Desktop](https://docs.docker.com/desktop/).

### Linux
* Install [Docker Engine](https://docs.docker.com/engine/install/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)
* Install [Docker Desktop](https://docs.docker.com/desktop/install/linux-install/)

## Development build
Make a copy of [the file](https://github.com/Amsterdam-Music-Lab/MUSCLE/blob/develop/.env.dist) `.env.dist` (in the same directory as this README) and rename it to `.env.` This file contains variables used by Docker to start up a container network serving MUSCLE.

Start Docker (the app icon is a whale carrying containers). Then, open a terminal and run
`docker compose up` (add `sudo` on Linux).
This command starts up the containers defined in `docker compose.yaml`:
- a PostgreSQL container, for storing experiment/user/playlist data, saved on the host machine in the Docker user data, represented in the volume `db_data`. Data added to the database will persist if the container is shut down.
- a ip2country container, which provides country codes for ip addresses, used for demographic information of users.
- a container of the server, defined in DockerfileDevelop in `backend`. The Dockerfile defines the Python version and installs development dependencies. The startup command runs migrations and then starts up a Django development server.
- a container of the client, defined in DockerfileDevelop in `frontend`. The Dockerfile defines the node version and installs node modules. The startup command kicks off a React development server.

Once you see all containers have started up, open your browser and navigate to [localhost:3000](http://localhost:3000). You should now be able to see the first screen of the Goldsmiths Musical Sophistication Index questionnaire.

Since the `docker compose.yaml` defines bind mounts for `backend` and `frontend`, any changes to the files on the host are immediately reflected in the containers, which means code watching works and hot reload works in the same way as with a native node or Django server.

To stop the containers, press `ctrl-c` or (in another terminal) run
`docker compose down`.

## Production build
A production build should define its own `docker compose.yaml`, making use of the `Dockerfile` of the `backend` and `frontend` environments. It should also define a custom .env file, with safe passwords for the SQL database and the Python backend. Instead of mounting the entire backend and frontend directory and using the development servers, the backend should serve with gunicorn, and the frontend should use a build script to compile static html, css and JavaScript.

## Troubleshooting

Please refer to the [wiki](https://github.com/Amsterdam-Music-Lab/MUSCLE/wiki/X.-Troubleshooting) a checklist of common issues and their solutions.
