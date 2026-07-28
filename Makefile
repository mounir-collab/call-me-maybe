NAME = call-me-maybe

PYTHON = python
UV = uv

MAIN = src

.PHONY: all install run debug clean lint lint-strict

all: run

install:
	$(UV) sync

run:
	$(UV) run $(PYTHON) -m $(MAIN)

debug:
	$(UV) run $(PYTHON) -m pdb -m $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

lint:
	$(UV) run flake8 src
	$(UV) run mypy src \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(UV) run flake8 src
	$(UV) run mypy src --strict