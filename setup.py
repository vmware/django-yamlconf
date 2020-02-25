#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

import codecs
from os import path
from setuptools import setup

README = """
django-yamlconf
===============

``django_yamlconf`` is part of VMware's support of open source
development and community.

Handle YAML based Django settings: load Django settings from YAML files
based on a Django project name. The YAML files loaded start with a YAML
file in the directory containing the Django settings file and then loads
any other YAMLCONF files up the directory tree from the initial file.
Values from files higher up the directory tree over-ride lower in the
tree. The contents of the YAML file simply defines values that over-ride
(or add to) attributes of the standard Django settings file, e.g., for
the project "buildaudit", the settings.py file could contain:

.. code:: python

        DEBUG = True

i.e., the value for development. This can be redefined via a
``buildaudit.yaml`` file using the definition:

.. code:: python

        DEBUG: false

If the environment variable ``YAMLCONF_CONFFILE`` is defined, it uses as
the final YAML file loaded (in this case, the file name does not need to
match the project name and it can be located anywhere in the file
system).

Quick Start
-----------

The YAMLCONF definitions are added to the Django settings file by
including a call to the ``load`` function in the settings file. This
would normally be towards the end of the settings file. The simplest,
and likely normal usage is to call without arguments. YAMLCONF will
infer the project information from the call stack. For a standard Django
application structure, the settings file::

        myproject/myproject/settings.py

would contain the development oriented definitions, e.g., database
definitions for user and password for a development database. The
settings file would then end with a call the the ``load`` function.
Additional definitions could be defined after the ``load`` function to
update conditional definitions, e.g., if ``DEBUG`` is enabled.

.. code:: python

    import django_yamlconf

    ...

    DATABASES = {
        'default': {
            'NAME': 'example',
            'USER': 'example',
            'PASSWORD': 'example',
            'HOST': 'localhost',
            ...
        }
    }
    ...

    django_yamlconf.load()

On a production server, for this example, a ``myproject.yaml`` would be
put in place containing the host name for the production database and
the password for the example user (assuming production is using the same
database name and username). In this example, a random ``pwgen``
password is used:

.. code:: yaml

    DATABASES.default.PASSWORD: 'zibiemohjuD6foh0'
    DATABASES.default.HOST: 'myproject-db.eng.vmware.com'

See the ``load`` function for more information on other optional
arguments.

License
-------

``django-yamlconf`` is release under the BSD-2 license, see the LICENSE
file.

SPDX-License-Identifier: BSD-2-Clause
"""

def version():
    vers_path = path.join(
        path.dirname(__file__),
        "django_yamlconf",
        "VERSION"
    )
    with open(vers_path, "r") as fh:
        v_info = fh.readline()
    return ".".join(filter(lambda x: x != '', v_info.split(" "))).strip()


setup(
    name='django-yamlconf',
    version=version(),
    author='Michael Rohan',
    author_email='mrohan@vmware.com',
    description='Define Django settings in local YAML (or JSON) files',
    long_description=README,
    license='BSD-2',
    platforms=['Any'],
    keywords=['django'],
    url='https://github.com/vmware/django-yamlconf',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Framework :: Django",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 2.0",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.7',
        'PyYAML>=3.10',
        'six>=1.10.0',
    ],
    packages=[
        'django_yamlconf',
        'django_yamlconf.templatetags',
        'django_yamlconf.management',
        'django_yamlconf.management.commands',
    ],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose', 'Jinja2'],
)
