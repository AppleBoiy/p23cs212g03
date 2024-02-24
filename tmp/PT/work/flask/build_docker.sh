#!/bin/sh

# read the environment variables from .env.dev
[ -e "$PWD"/.env.dev ] && . "$PWD"/.env.dev


app="docker.test"
docker build -t ${app} .
docker run -p 56733:8000 -d \
  --name=${app} \
  -e FLASK_DEBUG=${FLASK_DEBUG} \
  -v $PWD:/flask_app ${app}
