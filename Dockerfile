# pull official base image
FROM python:3.8.1-alpine

# set working directory
WORKDIR /usr/src/app

#install dependencies

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev &&\
    apk add postgresql-dev && \
    apk add netcat-openbsd

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . .
