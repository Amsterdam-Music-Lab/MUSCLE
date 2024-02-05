FROM docker.io/python:3.8
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get install -y ffmpeg
RUN apt-get install -y gettext

WORKDIR /server
COPY requirements/prod.txt /server/
RUN pip install -r prod.txt

# Add the dev tools if AML_DEBUG is set to true
ARG AML_DEBUG=false
RUN if [ "$AML_DEBUG" = "true" ] ; then pip install django-debug-toolbar ; fi

# We add remainig code later, so pip install won't need to rerun if source code changes
COPY . /server/