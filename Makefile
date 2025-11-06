# -*- coding: utf-8 -*-
# Copyright © 2018-2025, Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

# Utility Makefile to package, clean and test
PYTHON=python3
VENV=.venv
VENVDISTRO=.venv-distro
ACTIVATE=. $(VENV)/bin/activate
PYTEST=$(VENV)/bin/pytest

distro:
	if [ ! -d $(VENVDISTRO) ]; then $(PYTHON) -m venv $(VENVDISTRO); fi
	. $(VENVDISTRO)/bin/activate && pip install -U pip
	. $(VENVDISTRO)/bin/activate && pip install build
	. $(VENVDISTRO)/bin/activate && pip install twine
	. $(VENVDISTRO)/bin/activate && $(PYTHON) -m build

publish:	clean distro
	. $(VENVDISTRO)/bin/activate && $(PYTHON) -m twine upload

documentation:	$(VENV)
	$(ACTIVATE) && $(MAKE) -C docs html

check:	$(VENV)
	$(ACTIVATE) && PYTHONPATH=.:src $(PYTEST) tests

tox-check:	$(VENV)
	$(ACTIVATE) && tox

coverage:	$(VENV)
	$(ACTIVATE) && PYTHONPATH=.:src coverage run --source=src/django_yamlconf/ $(PYTEST) tests
	$(ACTIVATE) && coverage html

style-check:	$(VENV)
	$(ACTIVATE) && pycodestyle `find src tests -name '*.py'`
	$(ACTIVATE) && find src tests -name '*.py' | xargs pyflakes
	$(ACTIVATE) && find src -name '*.py' | xargs pylint

venv $(VENV):
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install -U pip
	$(ACTIVATE) && pip install -r requirements.txt

clean:
	find src -name __pycache__ | xargs rm -rf
	find src -name '*.pyc' | xargs rm -f
	rm -rf django_yamlconf.egg-info
	rm -rf django_yamlconf/root
	rm -f .coverage
	rm -rf htmlcov
	rm -rf $(VENVDISTRO) $(VENV)
	rm -rf .venv?
	rm -rf .eggs
	rm -rf .tox
	rm -rf build
	rm -rf dist
	$(MAKE) -C examples $@
	$(MAKE) -C docs $@
