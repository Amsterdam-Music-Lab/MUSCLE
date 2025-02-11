# Running commands in the docker containers

There are a few different methods to run commands in the docker containers.

## Running commands from the local terminal

To run a command in the server container you can use:

`docker compose run server --rm <command>`

To run a command in the postgresql container you can use:

`docker compose run db --rm <command>`

### Methods of running commands:

`docker compose run`

- Creates and starts a new container from a specified image.
- Can run a command in the new container.
- Useful for running one-off tasks or starting new containers.

[Click here for info on `docker compose run`](https://docs.docker.com/reference/cli/docker/compose/run)

`docker compose exec`

- Runs a command in an already running container.
- Does not create a new container.
- Useful for running commands or opening a shell in an existing container.

[Click here for info on `docker compose exec`](https://docs.docker.com/reference/cli/docker/compose/exec)

## Running commands via the docker desktop terminal

- Open docker desktop
- Click `containers`in the left panel
- CLick the 3 dots in the `actions` column of the container
- Click `open in terminal`

Now you can run your commands directly in the terminal of the container.

## Attach VScode to a container to run commands

- Open a new window with VScode
- Click `View` then `Command Palette`
- Search for `Dev Containers: Attach to Running Container`
- Click the container you want to attach to VScode

Now you can use VScode's terminal to run commands directly in the container.

[Click here for more info](https://code.visualstudio.com/docs/devcontainers/attach-container)
