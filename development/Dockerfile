ARG PYTHON_VER

FROM python:${PYTHON_VER}-slim

RUN pip install --upgrade pip \
  && pip install poetry

WORKDIR /source
COPY pyproject.toml /source

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
