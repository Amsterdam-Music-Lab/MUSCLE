FROM docker.io/python:3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /mkdocs
COPY pyproject.toml .
RUN uv lock
RUN uv sync --locked
COPY mkdocs.yml .
RUN mkdir docs
COPY *.md ./docs
EXPOSE 8080
CMD uv run mkdocs serve