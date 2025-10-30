# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Simple test of setting an individual literal value.
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestAddAttrs(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        self.settings.X = "x"
        django_yamlconf.load(project="testing", settings=self.settings)
        django_yamlconf.add_attributes(
            self.settings,
            {"A": "a", "B": "{A}b", "ETC_DIR": "{TOP_DIR}/etc"},
            "**TESTING**",
        )

    def test_a(self):
        """
        Value of A should be "a"
        """
        self.assertEqual(self.settings.A, "a")

    def test_b(self):
        """
        Value of B should be "ab"
        """
        self.assertEqual(self.settings.B, "ab")

    def test_etc_dir(self):
        """
        Verify of ETC_DIR => {TOP_DIR}/etc
        """
        self.assertEqual(
            self.settings.ETC_DIR, "{0}/etc".format(TestAddAttrs.TOP_DIR)
        )

    def test_x(self):
        """
        Value of X should be "x"
        """
        self.assertEqual(self.settings.X, "x")
