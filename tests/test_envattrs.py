# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test definition of attributes via env. variables
"""

import os

import django_yamlconf
from tests import MockSettings
from tests import YCTestCase


class TestDefAttrs(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        os.environ["YAMLCONF_A"] = "a"
        os.environ["YAMLCONF_B"] = "{A}b"
        django_yamlconf.load(project="testing", settings=self.settings)

    def tearDown(self):
        """
        Remove the environment variables
        """
        del os.environ["YAMLCONF_A"]
        del os.environ["YAMLCONF_B"]

    def test_env_a(self):
        """
        Value of A from environment
        """
        self.assertEqual(self.settings.A, "a")

    def test_env_b(self):
        """
        Value of B from environment
        """
        self.assertEqual(self.settings.B, "ab")
