# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test the "ycexplain" management command
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestInvalidYAML(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()

    def test_invalid_format(self):
        """
        Verify message for an invalid YAML format
        """
        if hasattr(self, "assertLogs"):
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.load(
                    project="invalid", settings=self.settings
                )
                self.assertIn("Failed to load", logs.output[0])

    def test_invalid_data(self):
        """
        Verify message for an invalid YAML data
        """
        if hasattr(self, "assertLogs"):
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.load(
                    project="lists", settings=self.settings
                )
                self.assertIn(
                    "did not define a dictionary", logs.output[0]
                )
