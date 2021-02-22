install:
	@poetry install

test:
	poetry run pytest --cov=page_loader tests/ --cov-report xml

lint:
	poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck lint

build: check
	@poetry build

.PHONY: install test lint selfcheck check build
