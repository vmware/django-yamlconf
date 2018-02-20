# -*- coding: utf-8 -*-
# Copyright © 2018, VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

# Utility Makefile to package, clean and test
PYVER=3
VENV=.venv$(PYVER)
ACTIVATE=. $(VENV)/bin/activate

distro:
	setup.py sdist

check:	$(VENV)
	$(ACTIVATE) && setup.py test

coverage:	$(VENV)
	$(ACTIVATE) && coverage run --source=django_yamlconf/ setup.py test
	$(ACTIVATE) && coverage html

style-check:	$(VENV)
	$(ACTIVATE) && pycodestyle ``find django_yamlconf -name '*.py'`
	find django_yamlconf -name '*.py' | xargs pyflakes
	find django_yamlconf -name '*.py' | grep -v tests | xargs pylint

venv $(VENV):
	virtualenv --python=python$(PYVER) $(VENV)
	$(ACTIVATE) && pip install -r requirements.txt

clean:
	$(MAKE) -C examples $@
	find django_yamlconf -name __pycache__ | xargs rm -rf
	find django_yamlconf -name '*.pyc' | xargs rm -f
	rm -rf django_yamlconf.egg-info
	rm -rf django_yamlconf/root
	rm -f .coverage
	rm -rf htmlcov
	rm -rf .venv?
	rm -rf .eggs
	rm -rf build
	rm -rf dist
