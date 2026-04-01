COMPOSE := docker compose

.PHONY: up down logs migrate makemigrations backend-shell db-shell restart ps seed-demo

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

restart:
	$(COMPOSE) restart

migrate:
	$(COMPOSE) exec backend alembic upgrade head

makemigrations:
	$(COMPOSE) exec backend alembic revision --autogenerate -m "$${m:-update_schema}"

backend-shell:
	$(COMPOSE) exec backend bash

db-shell:
	$(COMPOSE) exec db psql -U postgres -d virtual_closet

seed-demo:
	$(COMPOSE) exec backend python scripts/seed_demo.py
