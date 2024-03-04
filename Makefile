# silent makefile
.SILENT:

seed-db:
	bash ./scripts/seed_db.sh

chmod:
	find . -name "*.sh" -exec chmod 700 {} \;

dos2unix:
	find . -type f -name "*.sh" -exec dos2unix {} \;

unix2dos:
	find . -type f -name "*.sh" -exec unix2dos {} \;

build: chmod
	docker compose -f docker-compose.yml build && docker compose -f docker-compose.yml --compatibility up -d

remote-db:
	bash ./scripts/remote_db.sh

remote-dk:
	bash ./scripts/attach_docker.sh

format:
	bash ./scripts/format.sh

prune-dk:
	docker system prune -a -f