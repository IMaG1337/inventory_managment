up:
	docker compose -f docker-compose.yml up -d web telegram

down:
	docker compose down -v
