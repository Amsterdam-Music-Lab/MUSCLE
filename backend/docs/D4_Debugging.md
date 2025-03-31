# Debugging

If all containers are running via docker-compose, it is not possible to interact with the debug shell. Therefore, you need to do the following:

1. `docker ps` to list all running containers

2. `docker rm -f name_of_server_container`

3. `docker-compose run --rm --service-ports server`

After that, if you place a `breakpoint()` anywhere in the code, you can step through and inspect values of variables.