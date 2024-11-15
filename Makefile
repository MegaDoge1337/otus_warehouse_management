PHONY: domain-test, infra-test, lint, format import-sort


domain-test:
	python -m unittest ./tests/test_domain/test_services.py

infra-test:
	python -m unittest ./tests/test_infrastructure/test_orm.py

format:
	poetry run black .

lint:
	poetry run ruff check

import-sort:
	poetry run isort .
