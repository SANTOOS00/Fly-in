MAIN = main.py

VENV = .venv# 5asni n3rf axno huya '.'

MAP_DEF = maps/challenger/01_the_impossible_dream.txt

REQ = requirement.txt

PYTHON3_PATH = $(VENV)/bin/python3

PYTHON3 = python3

PIP_PATH = $(VENV)/bin/pip

CACH = __pycache__ .mypy_cache .flake8

env:
	@if [ ! -d "$(VENV)" ]; then $(PYTHON3) -m venv $(VENV); fi

run: env# IS VALID LINE
	$(VENV)/bin/python3 $(MAIN) $(MAP_DEF)

install: env
	$(PIP_PATH) install -r $(REQ)

clean:
	rm -rf $(CACH)
	echo "Cleaned cache files!"

lint:
	@flake8 .
	@mypy . --warn-return-any\
	--warn-unused-ignores\
	--ignore-missing-imports\
	--check-untyped-defs
	--disallow-untyped-defs\











# PYTHON = python3
# VENV = .venv

# REQUIREMENT = requirement.txt

# VENV_BIN = $(VENV)/bin

# PYTHON_PATH = $(VENV_BIN)/python

# PIP_PATH = $(VENV_BIN)/pip

# RM = rm

# RM_FLAGS = -rf

# CACHE = ./__pycache__ .mypy_cache .flake8

# DEFAULT_MAP = ./maps/challenger/01_the_impossible_dream.txt

# FILES = ./Graph.py Log.py ./Path.py ./Interfaces.py  ./Errors.py ./Parser.py \
# 				./Enums.py  ./Dijkstra.py ./Colors.py ./Simulation.py  ./Validator.py \
# 				./FileReader.py ./Singleton.py ./Mettadata.py ./main.py ./GraphBuilder.py

# PYTHON = python3
# VENV = .venv

# REQUIREMENT = requirement.txt

# VENV_BIN = $(VENV)/bin

# PYTHON_PATH = $(VENV_BIN)/python

# PIP_PATH = $(VENV_BIN)/pip

# RM = rm

# RM_FLAGS = -rf

# CACHE = ./__pycache__ .mypy_cache .flake8

# DEFAULT_MAP = ./maps/challenger/01_the_impossible_dream.txt

# FILES = ./Graph.py Log.py ./Path.py ./Interfaces.py  ./Errors.py ./Parser.py \
# 				./Enums.py  ./Dijkstra.py ./Colors.py ./Simulation.py  ./Validator.py \
# 				./FileReader.py ./Singleton.py ./Mettadata.py ./main.py ./GraphBuilder.py

# MAIN = main.py

# MYPY = mypy

# MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs

# run: env 
# 	$(PYTHON_PATH) $(MAIN) $(DEFAULT_MAP)

# env: # create virtual enviroment
# 	@if [ ! -d "$(VENV)" ]; then $(PYTHON) -m venv $(VENV); fi

# install: env
# 	@$(PIP_PATH) install -r $(REQUIREMENT)


