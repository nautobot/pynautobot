ARG PYTHON_VER

FROM python:${PYTHON_VER}-slim

RUN apt-get -y update && apt-get -y install --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install specific version of Poetry (1.8.5)
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.5 python3 - && \
    /root/.local/bin/poetry config virtualenvs.create false

WORKDIR /source
COPY . /source/

RUN git config --global --add safe.directory /source

RUN /root/.local/bin/poetry install --no-interaction --no-ansi
