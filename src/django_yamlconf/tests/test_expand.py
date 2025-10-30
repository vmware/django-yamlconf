# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test expansion of attribute references.
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestExpand(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        django_yamlconf.load(project="expand", settings=self.settings)

    def test_simple_expand(self):
        """
        Simple expand A: 'a{B}', B: 'b' => A = 'ab'
        """
        self.assertEqual(self.settings.A, "ab")

    def test_etc_dir(self):
        """
        Expanded path including TOP_DIR: ETC_DIR
        """
        self.assertEqual(self.settings.ETC_DIR, f"{TestExpand.TOP_DIR}/etc")

    def test_recurse_x(self):
        """
        Definition of mutal recusive X should be {Y}
        """
        self.assertEqual(self.settings.X, "{Y}")

    def test_recurse_y(self):
        """
        Definition of mutal recusive Y should be {X}
        """
        self.assertEqual(self.settings.Y, "{X}")

    def test_invalid_format(self):
        """
        Test error message for invalid attr reference
        """
        if hasattr(self, "assertLogs"):
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.add_attributes(
                    self.settings,
                    {"X": "Reference to invalid {ATTR"},
                    "**TESTING**",
                )
                self.assertIn("Invalid format", "\n".join(logs.output))

    def test_missing_key(self):
        """
        Test error message for invalid attr name
        """
        if hasattr(self, "assertLogs"):
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.add_attributes(
                    self.settings,
                    {"X": "Reference to undefined {NO_SUCH_ATTR}"},
                    "**TESTING**",
                )
                self.assertIn(
                    "Reference to undefined", "\n".join(logs.output)
                )
