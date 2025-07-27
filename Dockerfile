
# Dockerfile
# Usa python 3.12.8 y poetry 1.7.1
# Guarda este contenido como Dockerfile en la raíz del proyecto

# syntax=docker/dockerfile:1
FROM python:3.12.8-slim

ENV POETRY_VERSION=1.7.1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl build-essential && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Añadir poetry al PATH
ENV PATH="/root/.local/bin:$PATH"

# Crear directorio de la app
WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root

COPY . /app
