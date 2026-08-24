PYTHON ?= python
COMPOSE ?= docker compose --env-file .env.example

.PHONY: install install-dev check lint test coverage smoke docker-config docker-build clean

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pip-tools==7.6.1
	$(PYTHON) -m piptools sync requirements.txt

install-dev:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pip-tools==7.6.1
	$(PYTHON) -m piptools sync requirements.txt requirements-dev.txt

check:
	$(PYTHON) -m pip check
	$(PYTHON) -m piptools compile --dry-run requirements.in
	$(PYTHON) -m piptools compile --dry-run requirements-dev.in

lint:
	ruff check backend alembic

test:
	pytest backend/tests -q

coverage:
	pytest backend/tests \
		--cov=ml \
		--cov=app.inference \
		--cov-report=term-missing \
		--cov-fail-under=85 \
		-q

smoke:
	bash scripts/smoke.sh

docker-config:
	$(COMPOSE) config --quiet

docker-build:
	$(COMPOSE) build api

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
