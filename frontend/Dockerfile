# Base image
FROM docker.io/node:22-alpine as base

WORKDIR /client
RUN yarn set version 4.1.1
COPY package.json /client/
COPY yarn.lock /client/
COPY jsconfig.json /client/
RUN yarn

FROM base as dev
COPY tsconfig.json /client/
COPY tsconfig.node.json /client/
COPY vite.config.ts /client/
COPY vite-env.d.ts /client/
COPY vitest.config.ts /client/
COPY index.html /client/

FROM base as prod
COPY . /client/
RUN yarn build

# Runner image that serves the built app using nginx
FROM docker.io/nginx:alpine as runner

COPY --from=builder /client/build /usr/share/nginx/html
EXPOSE 80