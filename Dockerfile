# syntax=docker/dockerfile:1
FROM python:3.12.8-slim

ENV POETRY_VERSION=1.7.1

RUN apt-get update && apt-get install -y \
    curl build-essential tor gnupg && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

COPY . /app

# Expone el puerto local SOCKS
EXPOSE 9050

# Inicia Tor en background, espera 5 segundos y corre tu script
CMD tor & sleep 5 && poetry run python main.py
