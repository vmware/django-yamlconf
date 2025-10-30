# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Simple test of setting an individual literal value.
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestNestedDict(YCTestCase):
    """
    Test class
    """

    def test_nested_dict(self):
        """
        Verify setting a value within nested dicts
        """
        settings = MockSettings()
        settings.X = {"Y": {"Z": 10}}
        django_yamlconf.add_attributes(
            settings, {"X.Y.Z": 20}, "**TESTING**"
        )
        self.assertEqual(settings.X["Y"]["Z"], 20)

    def test_create_nested_dict(self):
        """
        Verify nested dict's are created
        """
        settings = MockSettings()
        settings.X = {}
        django_yamlconf.add_attributes(
            settings, {"X.Y.Z": 20}, "**TESTING**"
        )
        self.assertEqual(settings.X["Y"]["Z"], 20)
