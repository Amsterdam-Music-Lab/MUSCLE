# Base image
FROM docker.io/node:22-alpine as base

WORKDIR /client
RUN yarn set version 4.1.1
COPY package.json /client/
COPY yarn.lock /client/
COPY jsconfig.json /client/

FROM base as dev
RUN yarn
COPY tsconfig.json /client/
COPY tsconfig.node.json /client/
COPY vite.config.ts /client/
COPY vite-env.d.ts /client/
COPY vitest.config.ts /client/
COPY eslint.config.mjs /client
COPY index.html /client/

FROM base as prod
RUN yarn
COPY . /client/
