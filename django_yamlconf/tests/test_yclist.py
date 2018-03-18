# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test the "ycexplain" management command
"""

from django.utils.six import StringIO

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestYCList(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        django_yamlconf.load(project="yclist", settings=self.settings)

    def test_yclist(self):
        """
        Verify output includes EXAMPLE attribute
        """
        if hasattr(self, "assertRegex"):
            out = StringIO()
            django_yamlconf.list_attrs(settings=self.settings, stream=out)
            self.assertRegex(out.getvalue(), "EXAMPLE *value")

    def test_yclist_no_settings(self):
        """
        Explain when YAMLCONF not initialized
        """
        if hasattr(self, "assertLogs"):
            with self.assertLogs('', level='ERROR') as logs:
                django_yamlconf.list_attrs(
                    settings=MockSettings(),
                    stream=StringIO(),
                )
                self.assertIn('No YAMLCONF attributes defined', logs.output[0])
