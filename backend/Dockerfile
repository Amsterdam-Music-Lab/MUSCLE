FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /server
COPY requirements/prod.txt /server/
RUN pip install -r prod.txt
# We add remainig code later, so pip install won't need to rerun if source code changes
COPY . /server/

