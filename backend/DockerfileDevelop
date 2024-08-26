FROM docker.io/python:3.11 AS base
ENV PYTHONUNBUFFERED=1
RUN apt-get -y update && apt-get install -y ffmpeg gettext graphviz graphviz-dev

WORKDIR /server
COPY requirements/dev.txt /server/
RUN pip install -r dev.txt
