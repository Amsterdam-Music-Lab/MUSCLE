FROM docker.io/python:3.12
RUN apt-get -y update && apt-get install -y ffmpeg gettext

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /server
COPY pyproject.toml .
RUN uv lock
RUN uv sync --group prod --locked

# We add remainig code later, so pip install won't need to rerun if source code changes
COPY . /server/
