SCRIPT = main.py
PYRIGHT = ./node_modules/.bin/pyright

MAP ?= maps/easy/01_linear_path.txt

all: run

run: install
	@python3 $(SCRIPT) $(MAP)

install:
	@pip install -r requirements.txt

clean:
	@rm -rf __pycache__ .mypy_cache .pytest_cache
	@echo "Cleaned cache files!"
	@rm -rf node_modules package-lock.json

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

check_error:
	$(PYRIGHT) $(NAME)
