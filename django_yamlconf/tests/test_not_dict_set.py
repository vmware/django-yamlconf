# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Simple test of setting an individual literal value.
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestNotDictSet(YCTestCase):
    """
    Test class
    """

    def test_set_non_key(self):
        """
        Check error when setting non dictionaries
        """
        if hasattr(self, "assertLogs"):
            settings = MockSettings()
            settings.X = "x"
            django_yamlconf.load(project="nosuchfile", settings=settings)
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.add_attributes(
                    settings, {"X.not_there": "a"}, "**TESTING**"
                )
                self.assertIn("Not a dictionary", logs.output[0])
