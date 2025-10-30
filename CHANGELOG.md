<!--
-*- coding: utf-8 -*-
    Copyright © 2019-2023, Broadcom, Inc.  All rights reserved.
    SPDX-License-Identifier: BSD-2-Clause
-->

## 1.5.0 - IN PROGRESS

* Use `SafeLoader` to load YAML files.

* Updates for Django 4 (use `path`, `re_path` instead of `url`).

* Migrated published docs to `.readthedocs.yaml` configuration file
  v2.

* Updated to pyproject.toml packaging and pytest testing.

* Various updates to dependencies highlighted by dependabot (mostly
  just noise in the examples directories).

* Dropped the `VERSION` file, the version information is defined in
  the Python sources now.

## 1.4.0 - 2021-03-03

* Added support for JSON encoded environment values if decorated with
  ":jsonenv".  If JSON decoding fails (invalid JSON string), the value
  is used as is.  This allows the definition of more complex values via
  the environment, list, dictionaries, etc.  This can be used in K8s
  environments, e.g., Concourse

* Added a `CODE-OF-CONDUCT` file for contributors.

## 1.3.0 - 2020-07-15

* Dropped explicit dependency on Django for package.  Overall project
  should include Django but also allows usage of package outside of a
  Django project.

* Update to support Django 3.0 (staticfiles -> static in template)

* Added Django 3.0 example (polls)

* Removed the Django 1.x example (polls)

## 1.2.1 - 2020-02-24

* Fix generation of the long description for the package.

## 1.2.0 - 2020-02-23

* Updates to support Django 3.0: Simply use "`six`" instead of the
  support "`django.utils.six`" package and use "`render`" instead of
  "`render_to_response`".

*  `ycsysfiles` should generate executable files if the source template
   file is executable.

* Ensure the absolute path is used when searching for YAML control
  files.  This issue is seen when running Django apps under uWSGI
  control.

* Added the built-in attribute `CPU_COUNT` (primarily for use in uWSGI
  ini files) giving the number of available CPUs.

## 1.1.0 - 2019-03-17

* Handle stricter loading for newer versions of PyYAML.  The warning
  "YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated" is
  generated referring to https://msg.pyyaml.org/load for full details.  The
  YAML load now specified Loader=FullLoader.

* The `defined_attributes` function now returns a dictionary with additional
  keys if the attribute defined is a nested dictionary, the top level
  dictionary from the setting file is now also added, e.g., if
  "DATABASES.default" is defined, the value returned will now have have a
  "DATABASES" key.

* Added `docs` directory and Sphinx infrastructure to support publishing
  to readthedocs.org

* Added support for a final, environment defined, YAML file defined
  via the environment variable `YAMLCONF_CONFFILE`

## 1.0.0 - 2018-08-13

Initial public release

## 0.x - 2018-08-07

Internal Broadcom releases
