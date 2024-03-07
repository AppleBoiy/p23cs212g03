#!/bin/sh

docker compose exec flask python3 manage.py create_db && \
docker compose exec flask python3 manage.py seed_courses && \
docker compose exec flask python3 manage.py seed_db && \
docker compose exec flask python3 manage.py seed_enrollments
