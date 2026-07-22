SCRIPT = main.py


MAP ?= maps/easy/03_basic_capacity.txt

# .PHONY: all run clean lint install debug

all: run

run:
	@python3 $(SCRIPT) $(MAP)

# debug:
# 	@python3 -m pdb $(SCRIPT) $(MAP)

install:
	@pip3 install -r requirements.txt

clean:
	@rm -rf __pycache__ .mypy_cache .pytest_cache
	@echo "Cleaned cache files!"
lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
