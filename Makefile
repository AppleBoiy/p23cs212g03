# silent makefile
.SILENT:

seed-db:
	bash ./scripts/seed_db.sh

drop-db:
	docker compose exec flask python3 manage.py drop_db || rm -rf ./postgres_data

chmod:
	find . -name "*.sh" -exec chmod 700 {} \;

dos2unix:
	find . -type f -name "*.sh" -exec dos2unix {} \;

unix2dos:
	find . -type f -name "*.sh" -exec unix2dos {} \;


build-web:
	docker compose -f docker-compose.yml build


rm-ds:
	find . -name ".DS_Store" -delete

create-db:
	docker compose -f docker-compose.yml --compatibility up -d

build: chmod dos2unix build-web create-db seed-db

remote-db:
	bash ./scripts/remote_db.sh

remote-dk:
	bash ./scripts/attach_docker.sh

format:
	bash ./scripts/format.sh

prune-dk:
	rm -rf ./postgres_data || sudo rm -rf ./postgres_data
	docker system prune -a -f