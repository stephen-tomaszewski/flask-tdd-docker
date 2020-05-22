# pull official nase image
FROM postgres:12-alpine

# run create.sql on init
# https://hub.docker.com/_/postgres/
# adds the .sql file to the docker folder to run on initialization
ADD create.sql /docker-entrypoint-initdb.d