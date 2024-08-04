FROM docker.io/python:3.11 as base
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update && apt-get install -y ffmpeg gettext

WORKDIR /server
COPY requirements/dev.txt /server/
RUN pip install -r dev.txt
