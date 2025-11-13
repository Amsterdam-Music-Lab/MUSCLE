# Builder image
FROM docker.io/node:18-alpine as builder

WORKDIR /client
RUN yarn set version 4.1.1
COPY package.json /client/
COPY yarn.lock /client/

RUN yarn
COPY jsconfig.json /client/
COPY tsconfig.json /client/
COPY tsconfig.node.json /client/
COPY vite.config.ts /client/
COPY lingui.config.js /client/
COPY index.html /client/
COPY src /client/src
# copy locale files to public folder
RUN cp -r src/locales /client/public/locales/