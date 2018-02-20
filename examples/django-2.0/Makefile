# -*- coding: utf-8 -*-
# Copyright © 2018, VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

#
# Makefile to run the example Django 2.0 application
#

VENV=venv
ACTIVATE=. $(VENV)/bin/activate
MANAGE=$(ACTIVATE); mysite/manage.py

all:
	@echo "Use 'make runserver' to run the example application"
	@echo "Use 'make yclist' to see an example YAMLCONF list"
	@echo "Use 'make ycexplain' to see an example YAMLCONF explain"
	@echo "Use 'make ycsysfiles' to see an example YAMLCONF sysfiles"

check runserver yclist:	$(VENV)
	$(MANAGE) $@

$(VENV):
	virtualenv --python=python3 $(VENV)
	$(ACTIVATE); pip install -r requirements.txt

clean:
	find mysite -name __pycache__ | xargs rm -rf
	rm -rf $(VENV)
