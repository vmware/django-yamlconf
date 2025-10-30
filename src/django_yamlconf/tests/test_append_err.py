# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test appending incompatiable types
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestAppendErr(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()

    def test_append_error(self):
        """
        Should reject appending dict to list
        """
        if hasattr(self, "assertLogs"):
            self.settings.DICT = {"a": 1, "b": 2}
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.load(
                    project="append", settings=self.settings
                )
                self.assertIn("Cannot append", logs.output[0])
