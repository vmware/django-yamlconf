# -*- coding: utf-8 -*-
# Copyright © 2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test the management comamnd yclist
"""

import django_yamlconf

from io import StringIO
from django.conf import settings
from django.core.management import call_command
from tests import YCTestCase


class MgmtCmdYcexplainTest(YCTestCase):

    def setUp(self):
        django_yamlconf.load(project="tests", settings=settings)

    def test_yclist_1(self):
        out = StringIO()
        call_command("ycexplain", "XMPL", stdout=out)
        self.assertIn('MPL = "Environment defined" (via', out.getvalue())
