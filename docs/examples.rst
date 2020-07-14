.. -*- coding: utf-8 -*-
   Copyright © 2019, VMware, Inc.  All rights reserved.
   SPDX-License-Identifier: BSD-2-Clause

.. _examples:

Examples
--------

The examples are based on the ``polls`` example from the `Django
Project <https://www.djangoproject.com/>`__ web site. There are two
flavors of this example:

1. Under Django version 2.0 in the directory ``examples/django-2.0``

The ``django-1.11`` directory has been removed as it is end of life and
GitHub is generating secuity issues on the old dependencies.

See the `Examples Directory on
GitHub <https://github.com/vmware/django-yamlconf/tree/master/examples>`__.

The examples for both versions of Django behaviour similarly: there are
``Makefile`` targets to:

-  ``init`` initialize a local SQLite database for the application
   (should be the first target executed, if experimenting.
-  ``runserver`` to run a local server
-  General utility targets for YAMLCONF: ``yclist``, ``ycexplain`` and
   ``ycsysfiles``.

An example of the usage of YAMLCONF, would be, e.g., in a production
environment, switching to a PostgreSQL database via the creation of a
``mysite.yaml`` file (would need to explicitly install the
``psycopg2-binary`` module):

.. code:: yaml

    DATABASES.default:
        ENGINE: django.db.backends.postgresql_psycopg2
        NAME: mysite
        USER: mysite
        PASSWORD: my-password
        HOST: localhost
        PORT: ''

