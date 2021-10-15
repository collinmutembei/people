# pull official base image
FROM python:3.10-slim-buster

LABEL org.opencontainers.image.title="collinmutembei/api-people" \
  org.opencontainers.image.description="API service for people information" \
  org.opencontainers.image.url="https://collinmutembei.dev/projects/api-service-template" \
  org.opencontainers.image.source="https://github.com/collinmutembei/api-people" \
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
ENV DATABASE_URL sqlite:///tmp/people.db

# install system dependencies
RUN apt-get update \
  && apt-get -y install gcc sqlite3 \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# add app
COPY src .

CMD uvicorn app.main:api --host 0.0.0.0 --port $PORT
