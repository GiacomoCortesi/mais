VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON := $(VENV)/bin/python
WORDKIR := openapi_server

LINT = flake8
FORMAT = autopep8 --in-place --aggressive --aggressive -r
REMOVE_UNUSED_IMPORTS = autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r

$(PYTHON):
	python3 -m venv $(VENV)

install: requirements.txt
	$(PYTHON) -m pip install -r requirements.txt

dev-install: dev-requirements.txt
	$(PYTHON) -m pip install -r dev-requirements.txt

lint:
	$(LINT) $(WORDKIR)

format: dev-install
	$(REMOVE_UNUSED_IMPORTS) $(WORDKIR)
	$(FORMAT) $(WORDKIR)
