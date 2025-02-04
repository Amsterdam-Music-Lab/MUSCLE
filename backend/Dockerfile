FROM docker.io/python:3.12
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update && apt-get install -y ffmpeg gettext

WORKDIR /server
COPY requirements/prod.txt /server/
RUN pip install -r prod.txt

# We add remainig code later, so pip install won't need to rerun if source code changes
COPY . /server/
