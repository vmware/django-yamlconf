# -*- coding: utf-8 -*-
# Copyright © 2018-2020, VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

#
# Makefile to run the example Django 2.0 application
#

VENV=venv
ACTIVATE=. $(VENV)/bin/activate
MANAGE=$(ACTIVATE); mysite/manage.py

all:
	@echo "Use 'make runserver' to run the example application"
	@echo "Use 'make init' to initial the DB and create super user"
	@echo "Use 'make yclist' to see an example YAMLCONF list"

check runserver shell yclist:	$(VENV)
	$(MANAGE) $@

init: $(VENV)
	$(MANAGE) migrate
	$(MANAGE) createsuperuser

$(VENV):
	virtualenv --python=python3 $(VENV)
	$(ACTIVATE); pip install -r requirements.txt

clean:
	find mysite -name __pycache__ | xargs rm -rf
	rm -rf $(VENV)
