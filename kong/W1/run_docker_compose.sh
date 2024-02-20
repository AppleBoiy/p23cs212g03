#!/bin/sh

docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml --compatibility up -d