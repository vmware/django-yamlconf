# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Simple test of setting an individual literal value.
"""

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestSimpleSets(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        self.settings.DICT1 = {}
        self.settings.DICT3 = {'v1': 'value1'}
        self.settings.LIST3 = [1, 2]
        self.settings.LIST4 = [1, 2]
        self.settings.LIST5 = [1, 2]
        self.settings.SCALAR = 10
        django_yamlconf.load(project="simplesets", settings=self.settings)

    def test_set_literal(self):
        """
        Set the EXAMPLE attribute to simple literal.
        """
        self.assertEqual(self.settings.EXAMPLE, "example")

    def test_set_dict_element1(self):
        """
        Set the DICT1[value] attribute to simple literal.
        """
        self.assertEqual(self.settings.DICT1['value'], "abc")

    def test_set_dict_element3(self):
        """
        Set the DICT2[v1] attribute to simple literal.
        """
        self.assertEqual(self.settings.DICT2['v1'], "value1")

    def test_set_dict_element2(self):
        """
        Set the DICT3[v2] attribute to simple literal.
        """
        self.assertEqual(self.settings.DICT3['v1'], "value1")
        self.assertEqual(self.settings.DICT3['v2'], "value2")

    def test_set_list1(self):
        """
        Set the LIST1 attribute to simple list value.
        """
        self.assertEqual(self.settings.LIST1, [1, 2])

    def test_set_list2(self):
        """
        Append to the LIST2 attribute to (undef)
        """
        self.assertEqual(self.settings.LIST2, [2017])

    def test_append_list3(self):
        """
        Append to the LIST3 attribute to (defined)
        """
        self.assertEqual(self.settings.LIST3, [1, 2, 2017])

    def test_append_list4(self):
        """
        Append to the LIST4 attribute to gives list
        """
        self.assertEqual(self.settings.LIST4, [1, 2, 2017])

    def test_prepend_list5(self):
        """
        Prepend to the LIST5 attribute to (defined)
        """
        self.assertEqual(self.settings.LIST5, [2017, 1, 2])

    def test_append_scalar(self):
        """
        Append to the SCALAR attribute gives list
        """
        self.assertEqual(self.settings.SCALAR, [10, 2017])

        self.settings.SCALAR = 10
