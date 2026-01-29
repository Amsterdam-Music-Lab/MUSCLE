# Builder image
FROM docker.io/node:22-alpine as builder

WORKDIR /client
RUN yarn set version 4.1.1
COPY package.json /client/
COPY yarn.lock /client/
COPY jsconfig.json /client/
COPY . /client/

# Copy .env file to break the cache
COPY .env /client/

RUN yarn
RUN yarn build

# Runner image that serves the built app using nginx
FROM docker.io/nginx:alpine as runner

COPY --from=builder /client/build /usr/share/nginx/html
EXPOSE 80