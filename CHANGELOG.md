<!--
-*- coding: utf-8 -*-
    Copyright © 2019, VMware, Inc.  All rights reserved.
    SPDX-License-Identifier: BSD-2-Clause
-->

## 1.1.0 - 2019-03-17

* Handle stricter loading for newer versions of PyYAML.  The warning
  "YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated" is
  generated referring to https://msg.pyyaml.org/load for full details.  The
  YAML load now specified Loader=FullLoader.

* The `defined_attributes` function now returns a dictionary with additional
  keys if the attribute defined is a nested dictionary, the top level
  dictionary from the setting file is now also added, e.g., if
  "DATABASES.default" is defined, the value returned will have a "DATABASES"
  key.

* Added `docs` directory and Sphinx infrastructure to support publishing
  to readthedocs.org

* Added support for a final, environment defined, YAML file defined
  via the environment variable `YAMLCONF_CONFFILE`

## 1.0.0 - 2018-08-13

Initial public release

## 0.x - 2018-08-07

Internal VMware releases
