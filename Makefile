DOCKER_COMPOSE = docker compose
SERVICE = telegram-bot

.PHONY: setup-dev fmt lint typecheck test all

setup-dev:
	$(DOCKER_COMPOSE) exec $(SERVICE) pip install –no-cache-dir -r requirements-dev.txt

fmt:
	$(DOCKER_COMPOSE) exec $(SERVICE) black –check .

lint:
	$(DOCKER_COMPOSE) exec $(SERVICE) ruff .

typecheck:
	$(DOCKER_COMPOSE) exec $(SERVICE) mypy src/

test:
	$(DOCKER_COMPOSE) exec $(SERVICE) pytest –maxfail=1 –disable-warnings -q

all: fmt lint typecheck test
