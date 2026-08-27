MAIN = main.py

VENV = .venv

MAP_DEF = maps/challenger/01_the_impossible_dream.txt

REQ = requirements.txt

PYTHON3 = python3

CACH = __pycache__ .mypy_cache

FILES = base_parse.py dijkstra.py graph.py \
		map.py parse_meta_data.py color.py \
		drones.py main.py parser_data.py \
		custom_error.py modules.py \
		parser.py simualtion.py

all:
	@echo "\nSolution: run the command 'make run'\n"

env:
	@if [ ! -d "$(VENV)" ]; then $(PYTHON3) -m venv $(VENV); fi

install: env
	@$(VENV)/bin/pip install -r $(REQ)

run: env
	@$(VENV)/bin/python3 $(MAIN) $(MAP_DEF)

clean:
	@rm -rf $(CACH) $(VENV)
	@echo "Cleaned cache files!"



lint: install env
	@$(VENV)/bin/flake8 $(FILES)
	@$(VENV)/bin/mypy $(FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --check-untyped-defs --disallow-untyped-defs

lint-strict: install env
	@$(VENV)/bin/flake8 $(FILES)
	@$(VENV)/bin/mypy $(FILES) --strict

debug: env
	@$(VENV)/bin/python3 -m pdb $(MAIN) $(MAP_DEF)