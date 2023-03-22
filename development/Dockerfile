ARG PYTHON_VER

FROM python:${PYTHON_VER}-slim

RUN apt-get -y update && apt-get -y install --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    /root/.local/bin/poetry config virtualenvs.create false

WORKDIR /source
COPY pyproject.toml /source

RUN git config --global --add safe.directory /source

RUN /root/.local/bin/poetry install --no-interaction --no-ansi
