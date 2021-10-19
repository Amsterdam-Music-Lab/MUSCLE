FROM node:14-alpine

WORKDIR /client
COPY package.json /client/
COPY yarn.lock /client/
RUN yarn
COPY . /client/
