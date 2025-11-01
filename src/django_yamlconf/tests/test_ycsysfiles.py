# -*- coding: utf-8 -*-
# Copyright © 2018-2025 Broadcom, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Test the "ycexplain" management command
"""

import codecs
import jinja2
import os

import django_yamlconf
from django_yamlconf.tests import MockSettings
from django_yamlconf.tests import YCTestCase


class TestYCSysfiles(YCTestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Initialize the mock settings object
        """
        self.settings = MockSettings()
        self.sysfiles_root = os.path.join(
            TestYCSysfiles.BASE_DIR, "tests/sys"
        )
        django_yamlconf.load(project="ycsysfiles", settings=self.settings)

    def test_test1(self):
        """
        Simple reference to an attribute
        """
        if hasattr(self, "assertLogs"):
            django_yamlconf.add_attributes(
                self.settings,
                {
                    "A": "a",
                    "YAMLCONF_SYSFILES_DIR": os.path.join(
                        self.sysfiles_root, "test1"
                    ),
                },
                "**TESTING**",
            )
            with self.assertLogs("", level="DEBUG") as logs:
                django_yamlconf.sysfiles(
                    create=False,
                    noop=True,
                    settings=self.settings,
                    render=self.render,
                )
                self.assertIn("Value of A is a.", "\n".join(logs.output))

    def test_test2(self):
        """
        Reference to a dictionary based attribute
        """
        if hasattr(self, "assertLogs"):
            self.settings.DATABASES = {}
            django_yamlconf.add_attributes(
                self.settings,
                {
                    "DATABASES.default.PASSWORD": "Welcome",
                    "YAMLCONF_SYSFILES_DIR": os.path.join(
                        self.sysfiles_root, "test2"
                    ),
                },
                "**TESTING**",
            )
            with self.assertLogs("", level="DEBUG") as logs:
                django_yamlconf.sysfiles(
                    create=False,
                    noop=True,
                    settings=self.settings,
                    render=self.render,
                )
                self.assertIn(
                    "DB password is is Welcome.", "\n".join(logs.output)
                )

    def test_test3(self):
        """
        Generation of files: non-writeable
        """
        if hasattr(self, "assertLogs"):
            django_yamlconf.add_attributes(
                self.settings,
                {
                    "A": True,
                    "YAMLCONF_SYSFILES_DIR": os.path.join(
                        self.sysfiles_root, "test3"
                    ),
                },
                "**TESTING**",
            )
            with self.assertLogs("", level="DEBUG") as logs:
                django_yamlconf.sysfiles(
                    create=True,
                    noop=False,
                    settings=self.settings,
                    render=self.render,
                )
                self.assertIn(
                    "Skipping non-writeable or missing system file: "
                    + '"/myapp/tmpl.txt"',
                    "\n".join(logs.output),
                )

    def test_test4(self):
        """
        Generation of files: creationg
        """
        if hasattr(self, "assertLogs"):
            django_yamlconf.add_attributes(
                self.settings,
                {
                    "USE_A": True,
                    "A": "a",
                    "YAMLCONF_SYSFILES_DIR": os.path.join(
                        self.sysfiles_root, "test4"
                    ),
                },
                "**TESTING**",
            )
            with self.assertLogs("", level="DEBUG") as logs:
                rootdir = os.path.join(TestYCSysfiles.BASE_DIR, "root")
                django_yamlconf.sysfiles(
                    create=True,
                    noop=False,
                    settings=self.settings,
                    rootdir=rootdir,
                    render=self.render,
                )
                self.assertRegex(
                    " ".join(logs.output),
                    "Updating the system control file "
                    + '".*root.etc.xmpl.txt"',
                )

    def test_test5(self):
        """
        Generation of files: creating
        """
        if hasattr(self, "assertLogs"):
            django_yamlconf.add_attributes(
                self.settings,
                {
                    "ETC_DIR": "/var/oss/osstp/etc",
                    "A": "a",
                    "B": "b",
                    "YAMLCONF_SYSFILES_DIR": os.path.join(
                        self.sysfiles_root, "test5"
                    ),
                },
                "**TESTING**",
            )
            with self.assertLogs("", level="DEBUG") as logs:
                rootdir = os.path.join(TestYCSysfiles.BASE_DIR, "root")
                django_yamlconf.sysfiles(
                    create=True,
                    noop=False,
                    settings=self.settings,
                    rootdir=rootdir,
                    render=self.render,
                )
                self.assertRegex(
                    " ".join(logs.output),
                    "Updating the system control file "
                    + '".*root.var.oss.osstp.etc.xmpl.properties"',
                )

    def test_test6(self):
        """
        Missing sys files directory
        """
        if hasattr(self, "assertLogs"):
            django_yamlconf.add_attributes(
                self.settings,
                {
                    "A": "a",
                },
                "**TESTING**",
            )
            with self.assertLogs("", level="DEBUG") as logs:
                django_yamlconf.sysfiles(
                    create=False,
                    noop=True,
                    settings=self.settings,
                    render=self.render,
                )
                self.assertIn(
                    "No YAMLCONF_SYSFILES_DIR settings defined",
                    "\n".join(logs.output),
                )

    def test_test7(self):
        """
        Generation of files: execute bit set
        """
        if hasattr(self, "assertLogs"):
            django_yamlconf.add_attributes(
                self.settings,
                {
                    "YAMLCONF_SYSFILES_DIR": os.path.join(
                        self.sysfiles_root, "test7"
                    ),
                },
                "**TESTING**",
            )
            with self.assertLogs("", level="DEBUG") as logs:
                rootdir = os.path.join(TestYCSysfiles.BASE_DIR, "root")
                django_yamlconf.sysfiles(
                    create=True,
                    noop=False,
                    settings=self.settings,
                    rootdir=rootdir,
                    render=self.render,
                )
                self.assertRegex(
                    " ".join(logs.output),
                    "Adding execute permssions"
                )

    def render(self, source, attrs):
        """
        Full Django not available during testing, using the JINJA2
        templating directly.
        """
        with codecs.open(source, "r", "utf-8") as src:
            template = jinja2.Template(src.read())
        return template.render(attrs)
