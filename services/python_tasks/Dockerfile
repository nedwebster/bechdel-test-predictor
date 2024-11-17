FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# copy the poetry.lock and pyproject.toml file to the image
COPY uv.lock pyproject.toml /app/

# install dependencies without package
RUN uv sync --frozen --no-install-project --no-dev

# copy the app source code, and README.md for the poetry install command
COPY src/ /app/src/
COPY README.md /app/

# install package seperately for performance (according to UV)
RUN uv sync --frozen --no-dev

COPY services/python_tasks/scripts /app/scripts

ENV ENV=DOCKER

ENTRYPOINT ["uv", "run", "python"]