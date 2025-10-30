# -*- coding: utf-8 -*-
# Copyright © 2019 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Simple test the file defined by YAMLCONF_CONFILE is loaded.
"""

import os
import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestEnvFile(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        self.settings.XMPL = "Locally defined"
        os.environ["YAMLCONF_CONFFILE"] = os.path.join(
            os.path.dirname(__file__),
            "env.yaml",
        )
        django_yamlconf.load(project="xmpl", settings=self.settings)

    def test_set_xmpl(self):
        """
        Verify the value from the env.yaml file is used.
        """
        self.assertEqual(self.settings.XMPL, "Environment defined")
