.. -*- coding: utf-8 -*-
   Copyright © 2019, VMware, Inc.  All rights reserved.
   SPDX-License-Identifier: BSD-2-Clause

.. _format:

Support for Dictionaries
------------------------

YAMLCONF uses the "." character to identify attributes defined as part
of a dictionary, e.g., the DATABASES attribute. To set, e.g., the
password for a database connection:

.. code:: yaml

        DATABASES.default.PASSWORD: some-secret-password

It is considered an error if dotted name refers to a settings attribute
that is not an dictionary, the setting is ignored by YAMLCONF.

The dotted notation should be used to update dictionaries already
defined in the settings file. To add a new dictionary, a YAML dictionary
definition should be used, e.g.,:

.. code:: yaml

        NEW_DICTIONARY:
            key1: value1
            key2: value2

Attribute Substitution
----------------------

Frequently, attributes values are defined in terms of other attribute
values, most commonly using the base directory to define other
directories. The YAMLCONF allows other attributes to be referenced using
the Python named formatting syntax, e.g.,:

.. code:: yaml

        LOG_DIR: "{BASE_DIR}/log"

Currently only attributes defined via YAML files can be used in this
way. To disable this on a per-attribute basis, the ``:raw`` qualifier
should be defined to modify the behaviour for attribute, e.g.,:

.. code:: yaml

        LOGGING.formatters.simple.format: '%(asctime)s %(levelname)s %(message)s'
        LOGGING.formatters.simple.format:raw: True

Hiding values
-------------

The YAMLCONF includes an experimental view to handle URLs to display
attributes (should only be used in a debugging context), e.g., adding
the URL definition to your application::

    url(r'^yamlconf/', include('django_yamlconf.urls')),

will display the YAMLCONF attributes. For older versions of Django, the
``namespace`` needs to be explictly defined::

    url(r'^yamlconf/', include('django_yamlconf.urls', namespace='django_yamlconf')),

An example of the page displayed is:

.. figure:: images/yamlconf-list.png
   :alt: YAMLCONF Index Page

   Attributes Index Page

By default, any attribute value with the string ``PASSWORD`` in the name
will have their values hidden in the HTML displayed. Other, sensitive,
values can be explicitly hidden by defining the qualifier attribute
``:hide``, e.g.,:

.. code:: yaml

        APIKEY: 'my-api-key'
        APIKEY:hide: True

Extending Values
----------------

For list values, the qualifier attributes ``:prepend`` and ``:append``
can be used to extend the underlying definition, e.g., add another admin
user, the following definition can be used:

.. code:: yaml

        ADMINS:append: 'someuser@vmware.com'

The value of ``:prepend`` or ``:append`` qualified attribute can be
either a single value, as above, or a list of values. When a list is
given, the attribute is extend with the extra values, e.g.,:

.. code:: yaml

        ADMINS:append:
          - 'someuser1@vmware.com'
          - 'someuser2@vmware.com'

Normally, list values in the settings file are simply unordered lists.
There are, however, some values where the order matters, in particular,
the ``MIDDLEWARE`` list. A middleware that short-circuits the handling
of requests would need to be placed at the beginning of the list. This
is the rationale for the ``:prepend`` functionality.

Pre-defined Attributes
----------------------

The YAMLCONF module predefines the following attributes which can be
used, along with other attributed defined, via attribute substitution:

``BASE_DIR`` The directory containing the ``setting.py`` file

``PYTHON`` This is a dictionary giving the major, minor, micro,
releaselevel serial values for the Python interpretor

``OS_MACHINE`` The value of the ``platform.machine()`` function, e.g.,
``x86_64``

``OS_NODE`` The value of the ``platform.node()`` function, the system
short name

``OS_PROCESSOR`` The value of the ``platform.machine()`` function, e.g.,
``x86_64``

``OS_RELEASE`` The value of the ``platform.release()`` function, e.g.,
``4.4.0-101-generic``

``OS_SYSTEM`` The value of the ``platform.system()`` function, e.g.,
``Linux``

``TOP_DIR`` The directory above BASE\_DIR

``USER`` The login name of the current user

``VIRTUAL_ENV`` If run within a Python virtual environment, this
attribute is defined to be the path to the environment, otherwise it has
the value ``None``

Attribute Documentation
-----------------------

Appending ``:doc`` to an attribute name in a YAML file defines a
documentation string for the attribute. This should be used to give
information on the expected value for the attribute and how the value
might differ on production, beta and development servers, e.g.,
documentation for the DEBUG attribute would be defined using the YAML:

.. code:: yaml

        DEBUG:doc: |
            Enable or disable debugging functionality.  On the production server
            this attribute should be set to false

Typical Structure
-----------------

On a typical production system for the "buildaudit" app, a local
``buildaudit.yaml`` would exist in, e.g., the ``/var/www`` directory.
This would contain the production passwords, debug settings, etc. Under
this directory, a ``webapps`` directory could contain another
``buildaudit.yaml`` file possibly generated by a build process which
could define attributes identifying the build, the Git Hash for the
code, build time, etc. Finally, a ``buildaudit.yaml`` file co-located
with the settings.py file giving the base attributes and their
documentation strings::

        +- /var/www
            +- buildaudit.yaml
            +- webapps
               +- buildaudit.yaml
               +- buildaudit
                   +- buildaudit.yaml
                   +- settings.py


Environment Variables
---------------------

As a final source for values, the environment is queries for all environment
names beginning with ``YAMLCONF_``.  E.g., to "inject" the value "xyx" for the
setting "XYZ", the environment can be used::

    $ export YAMLCONF_XYZ=xyz

Environment variable values are pulled into the settings as a simple string
value.  For more complex values, the environment value can be interpreted
as a JSON encode structure if a setting with the ``:jsonenv`` qualifier is True
for the setting.  E.g., in a Fabric base deployment system, the servers to
deploy to can be defined in the base YAMLCONF file as:

.. code:: yaml

    DEPLOY_SERVERS:
      - '{DEPLOY_USER}@localhost'
    DEPLOY_USER: '{USER}'

I.e., deploy to ``localhost`` as the current user.  In a production environment,
the production servers would likely be a list of servers behind an HA-Proxy
server.  This list can be defined via a local YAMLCONF file in the directory
tree on the system where deployments are run.   A local file can, however, be
awkward in some contexts, e.g., deploy occurs as a Concourse job, and an
environment variable definition is easier.  In this case, the value can be
a JSON encoded value and JSON decode enabled via the ``:jsonenv`` qualifier.
The base YAMLCONF file would now include the definitions:

.. code:: yaml

    DEPLOY_SERVERS:
      - '{DEPLOY_USER}@localhost'
    DEPLOY_SERVERS:jsonenv: True

and the list of servers to deploy to "injected" via an environment variable::

    $ export YAMLCONF_DEPLOY_SERVERS='["{DEPLOY_USER}@host-a", "{DEPLOY_USER}@host-b"]'
