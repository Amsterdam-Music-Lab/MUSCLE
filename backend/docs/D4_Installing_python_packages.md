# Installing python packages

If you want to install new packages, you can do so by adding the dependencies to:

* `requirements.in/base.txt` for packages that are needed in both *development* **and** *production*

* `requirements.in/dev.txt` for packages that are only needed in *development*

* `requirements.in/prod.txt` for packages that are only needed in *production*

Then, run the following `pip-compile` commands to generate the `requirements.txt` files:

```bash
# update all packages for development
docker compose run --rm server pip-compile --output-file=requirements/dev.txt requirements.in/dev.txt

# Install all packages for production
docker compose run --rm server pip-compile --output-file=requirements/prod.txt requirements.in/prod.txt
```

This will check the `requirements.in` file, and:

- Check which versions are compatible with the current Python version
- Check which dependencies are needed for the packages listed in `requirements.in`
- Update `dev.txt` and/or `prod.txt` with the required packages

Lastly, rebuild the server image:

```bash
docker compose build server

# or, if you want to run the server immediately
docker compose up server --build -d
```
