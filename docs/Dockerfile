FROM docker.io/python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /docs

WORKDIR /docs
RUN uv sync --locked
CMD mkdocs build -d ./docs-pages-build