# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Base definitions to support testing.
"""

import os
from unittest import TestCase


class YCTestCase(TestCase):
    """
    Custom TestCase to "inject" the common attributes used for testing.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    TOP_DIR = os.path.dirname(BASE_DIR)


class MockSettings(object):
    """
    Empty class used as a substitute for a settings module for tests.
    """

    def __init__(self):
        pass
