# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Simple test of setting an individual literal value.
"""

import getpass
import platform

import django_yamlconf
from tests import MockSettings
from tests import YCTestCase


class TestPredefines(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        django_yamlconf.load(project="testing", settings=self.settings)

    def test_base_dir(self):
        """
        Verify predefined attribute `BASE_DIR`
        """
        self.assertEqual(self.settings.BASE_DIR, TestPredefines.BASE_DIR)

    def test_os_machine(self):
        """
        Verify predefined attribute `OS_MACHINE`
        """
        self.assertEqual(self.settings.OS_MACHINE, platform.machine())

    def test_os_node(self):
        """
        Verify predefined attribute `OS_NODE`
        """
        self.assertEqual(self.settings.OS_NODE, platform.node())

    def test_os_processor(self):
        """
        Verify predefined attribute `OS_PROCESSOR`
        """
        self.assertEqual(self.settings.OS_PROCESSOR, platform.processor())

    def test_os_release(self):
        """
        Verify predefined attribute `OS_RELEASE`
        """
        self.assertEqual(self.settings.OS_RELEASE, platform.release())

    def test_os_system(self):
        """
        Verify predefined attribute `OS_SYSTEM`
        """
        self.assertEqual(self.settings.OS_SYSTEM, platform.system())

    def test_top_dir(self):
        """
        Verify predefined attribute `TOP_DIR`
        """
        self.assertEqual(self.settings.TOP_DIR, TestPredefines.TOP_DIR)

    def test_user(self):
        """
        Verify predefined attribute `USER`
        """
        self.assertEqual(self.settings.USER, getpass.getuser())
