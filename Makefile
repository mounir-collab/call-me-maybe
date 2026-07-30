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


lint:
	$(UV) run flake8 $(MAIN)
	$(UV) run  mypy $(MAIN) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(UV) run flake8 $(MAIN)
	$(UV) run mypy $(MAIN) --strict