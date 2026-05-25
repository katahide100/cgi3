.PHONY: up down build watch logs

up:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

watch:
	./docker/dev-watch.sh

logs:
	docker compose logs -f
