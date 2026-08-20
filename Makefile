MAIN = main.py

VENV = .venv# 5asni n3rf axno huya '.'

MAP_DEF = maps/challenger/01_the_impossible_dream.txt

REQ = requirement.txt

PYTHON3_PATH = $(VENV)/bin/python3

PYTHON3 = python3

PIP_PATH = $(VENV)/bin/pip

CACH = __pycache__ .mypy_cache .flake8

FILES = *.py

all:
	@echo "\nSolution: run the command 'make run'\n"


env:
	@if [ ! -d "$(VENV)" ]; then $(PYTHON3) -m venv $(VENV); fi

run: env# IS VALID LINE
	@$(VENV)/bin/python3 $(MAIN) $(MAP_DEF)

install: env
	@$(PIP_PATH) install -r $(REQ)

clean:
	@rm -rf $(CACH) $(VENV)
	@echo "Cleaned cache files!"

lint:
	@flake8 .
	@mypy $(FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --check-untyped-defs --disallow-untyped-defs

lint-strict:
	@$(PYTHON_PATH) -m flake8 
	@$(PYTHON_PATH) -m $(MYPY) $(FILES) --strict

debug:
	&(PYTHON3_PATH) -m pdb $(FILES)