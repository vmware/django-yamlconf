# -*- coding: utf-8 -*-
# Copyright © 2018-2025, Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

# Utility Makefile to package, clean and test
VENV=.venv
VENVDISTRO=.venv-distro
ACTIVATE=. $(VENV)/bin/activate
PYTEST=$(VENV)/bin/pytest

distro:
	if [ ! -d $(VENVDISTRO) ]; then python3 -m venv $(VENVDISTRO); fi
	. $(VENVDISTRO)/bin/activate && pip install -U pip
	. $(VENVDISTRO)/bin/activate && pip install build
	. $(VENVDISTRO)/bin/activate && pip install twine
	. $(VENVDISTRO)/bin/activate && python3 -m build

publish:	clean distro
	if [ ! -d $(VENVDISTRO) ]; then python3 -m venv $(VENVDISTRO); fi
	. $(VENVDISTRO)/bin/activate && python3 -m twine upload

documentation:	$(VENV)
	$(ACTIVATE) && $(MAKE) -C docs html

check:	$(VENV)
	$(ACTIVATE) && $(PYTEST) src

tox-check:	$(VENV)
	$(ACTIVATE) && tox

coverage:	$(VENV)
	$(ACTIVATE) && coverage run --source=src/django_yamlconf/ $(PYTEST) src
	$(ACTIVATE) && coverage html

style-check:	$(VENV)
	$(ACTIVATE) && pycodestyle `find src -name '*.py'`
	$(ACTIVATE) && find src -name '*.py' | xargs pyflakes
	$(ACTIVATE) && find src -name '*.py' | grep -v tests | xargs pylint

venv $(VENV):
	python3 -m venv $(VENV)
	$(ACTIVATE) && pip install -U pip
	$(ACTIVATE) && pip install -r requirements.txt

clean:
	find django_yamlconf -name __pycache__ | xargs rm -rf
	find django_yamlconf -name '*.pyc' | xargs rm -f
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
