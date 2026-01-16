.PHONY: install format lint test clean build all

install:
	uv sync --active --all-groups

format:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff format --check .
	uv run ruff check .

test:
	(cd examples/portfolio-analytics && uv run pytest -n 4)

clean:
	rm -rf .venv .ruff_cache .pytest_cache dist
	find . -type d -name "__pycache__" -exec rm -rf {} +

build:
	uv build

all: install format link test
