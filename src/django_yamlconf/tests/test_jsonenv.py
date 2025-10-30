# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test definition of attributes via env. JSON variables
"""

import os

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestJsonEnv(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        os.environ["YAMLCONF_A"] = "[1, 2]"
        os.environ["YAMLCONF_B"] = '{"a": 1, "b": 2}'
        os.environ["YAMLCONF_C"] = "[1, 2"
        django_yamlconf.load(project="jsonenv", settings=self.settings)

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
        self.assertEqual(self.settings.A, [1, 2])

    def test_env_b(self):
        """
        Value of B from environment
        """
        self.assertEqual(self.settings.B["a"], 1)

    def test_env_c(self):
        """
        Value of C from environment: invalid JSON, it's a string!
        """
        self.assertEqual(self.settings.C, "[1, 2")
