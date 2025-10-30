# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test the "ycexplain" management command
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestInvalidLoader(YCTestCase):
    """
    Test using an invalid loader module
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()

    def test_non_existent(self):
        """
        Verify error for non-existent loader/syntax
        """
        if hasattr(self, "assertLogs"):
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.load(
                    project="nosuchfmt",
                    settings=self.settings,
                    syntax="nosuchfmt",
                )
                self.assertIn(
                    "Unsupported YAMLCONF format", logs.output[0]
                )

    def test_no_loader(self):
        """
        Verify error for loader/syntax without load method
        """
        if hasattr(self, "assertLogs"):
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.load(
                    project="nosuchfmt",
                    settings=self.settings,
                    syntax="os",
                )
                self.assertIn('has no "load"', logs.output[0])
