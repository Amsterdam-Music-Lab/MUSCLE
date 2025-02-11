# Running tests

## Frontend tests

To run the frontend tests, run the following command:

```sh
docker compose run --rm client yarn test --watchAll=false

# or use the script
./scripts/test-frontend
```

### Watch mode

To run the frontend tests in watch mode, which allows you to re-run tests when you change files, run the following command:

```sh
docker compose run --rm client yarn test

# or use the script
./scripts/test-frontend-watch
```

## Backend tests

To run the backend tests, run the following command:

```sh
docker compose run --rm server python manage.py test

# or use the script
./scripts/test-backend
```