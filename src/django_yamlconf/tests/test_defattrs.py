# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test return of defined_attributes
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestDefAttrs(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        django_yamlconf.load(project="defattrs", settings=self.settings)
        self.defattrs = django_yamlconf.defined_attributes(self.settings)

    def test_defined_attrs(self):
        """
        Defined attributes should be {'A': 'a', 'B': 'ab', ...}
        """
        self.assertEqual(self.defattrs["A"], "a")
        self.assertEqual(self.defattrs["B"], "ab")
        self.assertEqual(self.defattrs["C"], "abc")
        self.assertEqual(self.defattrs["D"], "abcd")

    def test_defined_attrs_names(self):
        """
        Defined attributes names should be ['A', 'B', ...]
        """
        self.assertEqual(
            sorted(self.defattrs.keys()),
            [
                "A",
                "B",
                "BASE_DIR",
                "C",
                "CPU_COUNT",
                "D",
                "OS_MACHINE",
                "OS_NODE",
                "OS_PROCESSOR",
                "OS_RELEASE",
                "OS_SYSTEM",
                "PYTHON",
                "TOP_DIR",
                "USER",
                "VIRTUAL_ENV",
            ],
        )

    def test_no_defined_attrs(self):
        """
        Expect empty set for no attributes
        """
        settings = MockSettings()
        self.assertEqual(django_yamlconf.defined_attributes(settings), {})
