# Builder image
FROM docker.io/node:18-alpine as builder

ARG VITE_STATIC_URL

WORKDIR /client
RUN yarn set version 4.1.1
COPY package.json /client/
COPY yarn.lock /client/
COPY jsconfig.json /client/
COPY . /client/

# Copy .env file to break the cache
COPY .env /client/

RUN yarn
# copy locale files to public folder
RUN cp -r src/locales public/locales/
# build with the base path set to VITE_STATIC_URL (to pull from CDN) or "/" as fallback
RUN yarn build --base ${VITE_STATIC_URL:-/}

# Runner image that serves the built app using nginx
FROM docker.io/nginx:alpine as runner

COPY --from=builder /client/build /usr/share/nginx/html
EXPOSE 80