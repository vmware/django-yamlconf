# -*- coding: utf-8 -*-
# Copyright © 2018, VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

#
# Makefile to run the example Django 1.11 application
#

VENV=venv
ACTIVATE=. $(VENV)/bin/activate
MANAGE=$(ACTIVATE); mysite/manage.py

all:
	@echo "Use 'make install' to update the Apache config"
	@echo "Use 'make init' to initial the DB and create super user"
	@echo "Use 'make runserver' to run the example application"
	@echo "Use 'make yclist' to see an example YAMLCONF list"
	@echo "Use 'make ycexplain' to see an example YAMLCONF explain"
	@echo "Use 'make ycsysfiles' to see an example YAMLCONF sysfiles"

check runserver yclist:	$(VENV)
	$(MANAGE) $@

init: $(VENV)
	$(MANAGE) migrate
	$(MANAGE) createsuperuser

install: $(VENV)
	$(MANAGE) collectstatic
	$(MANAGE) ycsysfiles

$(VENV):
	virtualenv --python=python2 $(VENV)
	$(ACTIVATE); pip install -r requirements.txt

clean:
	find mysite -name '*.pyc' | xargs rm -f
	rm -rf mysite/static-files
	rm -f mysite/sysfiles.txt
	rm -f mysite/mysite.log
	rm -rf $(VENV)
