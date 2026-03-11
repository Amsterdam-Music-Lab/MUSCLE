# This base Docker image is used to build a development image
# which is used in local development and CI/CD pipelines
FROM docker.io/python:3.12 AS base
ENV PYTHONUNBUFFERED=1
RUN apt-get -y update && apt-get install -y ffmpeg gettext
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /server
COPY pyproject.toml .
RUN uv lock
RUN uv sync --locked

FROM base AS dev
RUN uv sync --locked --group dev

FROM base AS prod
RUN uv sync --locked --group prod
COPY . /server/

# This graphviz Docker image is derived from the base image
# and installs extra dependencies for generating database diagrams
FROM base AS graphviz
RUN apt-get -y update && apt-get install -y graphviz graphviz-dev

# For generating database diagrams
RUN uv add pygraphviz django-extensions

# Generate graphviz image
# See also https://django-extensions.readthedocs.io/en/latest/graph_models.html
# for more options
ENTRYPOINT ["uv", "run", "python", "manage.py", "graph_models", "-a", "-g", "-o", "/server/static/model_graph.png"]
