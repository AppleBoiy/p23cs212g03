seed-db:
	bash ./scripts/seed_db.sh

chmod:
	find . -name "*.sh" -exec chmod 700 {} \;

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