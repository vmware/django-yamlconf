.. -*- coding: utf-8 -*-
   Copyright © 2019, VMware, Inc.  All rights reserved.
   SPDX-License-Identifier: BSD-2-Clause

.. _releases:

Releases & Major Branches
-------------------------

.. _releases-1.4.0:

Version 1.4.0
~~~~~~~~~~~~~

- Tagged with ``v1.4.0``.
- Added support for JSON encoded environment values if decorated with
  ``:jsonenv``.  If JSON decoding fails (invalid JSON string), the value
  is used as is.
- Added a ``CODE-OF-CONDUCT`` file for contributors.

.. _releases-1.3.0:

Version 1.3.0
~~~~~~~~~~~~~

- Tagged with ``v1.3.0``.
- Dropped explicit dependency on Django for package.  Overall project
  should include Django but also allows usage of package outside of a
  Django project.
- Update to support Django 3.0 (staticfiles -> static in template)
- Added Django 3.0 example (polls)
- Removed the Django 1.x example (polls)

.. _releases-1.2.1:

Version 1.2.1
~~~~~~~~~~~~~

- Tagged with ``v1.2.1``.
- Fix generation of the long description for the package.

.. _releases-1.2.0:

Version 1.2.0
~~~~~~~~~~~~~

- Tagged with ``v1.2.0``.
- Updates to support Django 3.0: Simply use "`six`" instead of the
  support "`django.utils.six`" package and use "`render`" instead of
  "`render_to_response`".
- `ycsysfiles` should generate executable files if the source template
  file is executable.
- Ensure the absolute path is used when searching for YAML control
  files.  This issue is seen when running Django apps under uWSGI
  control.
- Added the built-in attribute ``CPU_COUNT`` (primarily for use in uWSGI
  ini files) giving the number of available CPUs.

.. _releases-1.1.0:

Version 1.1.0
~~~~~~~~~~~~~

- Tagged with ``v1.1.0``.
- Handle stricter loading for newer versions of PyYAML.  The warning
  "YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated" is
  generated referring to https://msg.pyyaml.org/load for full details.  The
  YAML load now specified Loader=FullLoader.
- The ``defined_attributes`` function now returns a dictionary with additional
  keys if the attribute defined is a nested dictionary, the top level
  dictionary from the setting file is now also added, e.g., if
  "``DATABASES.default``" is defined, the value returned will now also have
  a "``DATABASES``" key.
- Added ``docs`` directory and Sphinx infrastructure to support publishing
  to readthedocs.org
- Added support for a final, environment defined, YAML file defined
  via the environment variable `YAMLCONF_CONFFILE`

.. _releases-1.0.0:

Version 1.0.0
~~~~~~~~~~~~~

- Initial public release (tagged with ``v1.0.0``)

