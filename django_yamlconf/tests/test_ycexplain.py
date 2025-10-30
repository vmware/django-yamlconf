# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test the "ycexplain" management command
"""

from six import StringIO

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestYCExplain(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        django_yamlconf.load(project="ycexplain", settings=self.settings)

    def test_ycexplain_missing(self):
        """
        Explain of unmanage attribute
        """
        out = StringIO()
        django_yamlconf.explain("X", settings=self.settings, stream=out)
        self.assertIn(
            'The setting "X" is not managed by YAMLCONF', out.getvalue()
        )

    def test_ycexplain_a(self):
        """
        Documentation for an attribute
        """
        out = StringIO()
        django_yamlconf.explain("A", settings=self.settings, stream=out)
        self.assertIn(
            'Example documentation for the attribute "A"', out.getvalue()
        )

    def test_ycexplain_b(self):
        """
        Explain expanded attribute
        """
        out = StringIO()
        django_yamlconf.explain("B", settings=self.settings, stream=out)
        self.assertIn("{A}", out.getvalue())
        self.assertIn("Value of A", out.getvalue())

    def test_ycexplain_not_managed(self):
        """
        Explain when YAMLCONF not initialized
        """
        if hasattr(self, "assertLogs"):
            with self.assertLogs("", level="ERROR") as logs:
                django_yamlconf.explain(
                    "X",
                    settings=MockSettings(),
                    stream=StringIO(),
                )
                self.assertIn(
                    "No YAMLCONF attributes defined", logs.output[0]
                )
