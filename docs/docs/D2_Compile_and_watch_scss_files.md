# Compile and watch scss files

The frontend container will build .css and .css.map files from scss every time you restart the Docker containers. To watch for and immediately see changes during development, run an extra client container like so:

`docker-compose run --rm client yarn scss-watch`