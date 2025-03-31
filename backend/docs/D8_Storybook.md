# Storybook

We have added a Storybook configuration for the React frontend of this website that allows researchers and stakeholders to look and play around with the components that are used in the experiments.

## What is Storybook?

> Storybook is a frontend workshop for building UI components and pages in isolation. Thousands of teams use it for UI development, testing, and documentation. It’s open source and free.

Source: [Storybook](https://storybook.js.org/)

## How to run Storybook?

You can either run Storybook in a Docker container, or on your local machine.

### Docker

```sh
docker exec -it muscle-client-1 yarn run storybook
```

### Local

```sh
cd frontend
yarn run storybook
```

### Build

You can also build a static website with Storybook that allows you to deploy it.

```sh
cd frontend
yarn run storybook:build
```

```
