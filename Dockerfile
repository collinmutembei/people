# pull official base image
FROM python:3.12.0-slim-bullseye

LABEL org.opencontainers.image.title="collinmutembei/people" \
  org.opencontainers.image.description="API service for people information" \
  org.opencontainers.image.url="=ghcr.io/collinmutembei/people" \
  org.opencontainers.image.source="https://github.com/collinmutembei/people" \
  org.opencontainers.image.revision="$COMMIT_ID" \
  org.opencontainers.image.version="$PROJECT_VERSION" \
  org.opencontainers.image.authors="Collin Mutembei (https://collinmutembei.dev)" \
  org.opencontainers.image.licenses="MIT"

# set working directory
WORKDIR /usr/api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# install system dependencies
RUN apt-get update \
  && apt-get -y install libmagic1 \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# add app
COPY src .

CMD uvicorn app.main:api --host 0.0.0.0 --port $PORT
