# -*- coding: utf-8 -*-
# Copyright © 2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test the URL views defined by YAMLCONF
"""

import pytest
import django_yamlconf

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from tests import YCTestCase


User = get_user_model()
_USERNAME = "testuser"
_ADMINNAME = "testadmin"
_PASSWORD = "welcome123"


@pytest.mark.django_db
class ViewTests(YCTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username=_USERNAME,
            password=_PASSWORD,
        )
        self.admin = User.objects.create_user(
            username=_ADMINNAME,
            password=_PASSWORD,
            is_staff=True,
        )
        django_yamlconf.load(project="tests", settings=settings)

    def test_no_access(self):
        self.client.login(username=_USERNAME, password=_PASSWORD)
        response = self.client.get(reverse("django_yamlconf:index"))
        self.assertEqual(response.status_code, 302)

    def test_index(self):
        self.client.login(username=_ADMINNAME, password=_PASSWORD)
        response = self.client.get(reverse("django_yamlconf:index"))
        self.assertEqual(response.status_code, 200)

    def test_attr_builtin(self):
        self.client.login(username=_ADMINNAME, password=_PASSWORD)
        response = self.client.get(
            reverse("django_yamlconf:attr", args=["CPU_COUNT"])
        )
        self.assertEqual(response.status_code, 200)

    def test_attr_yamldef(self):
        self.client.login(username=_ADMINNAME, password=_PASSWORD)
        response = self.client.get(
            reverse("django_yamlconf:attr", args=["XMPL"])
        )
        self.assertEqual(response.status_code, 200)

    def test_attr_notdef(self):
        self.client.login(username=_ADMINNAME, password=_PASSWORD)
        response = self.client.get(
            reverse("django_yamlconf:attr", args=["NO_SUCH_SETTING"])
        )
        self.assertEqual(response.status_code, 404)
