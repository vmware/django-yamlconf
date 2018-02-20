# -*- coding: utf-8 -*-
# Copyright © 2018, VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Update the system control files based on the current YAMLCONF settings values.
"""
from __future__ import unicode_literals

from django.conf import settings
from django_yamlconf import sysfiles
from django_yamlconf.management.commands import YCBaseCommand


class Command(YCBaseCommand):
    """
    Create the system control files needed to support application, e.g.,
    the Nginx config file (/etc/nginx/nginx.conf).  The control files
    created are all the template files under the directory defined by the
    setttings YAMLCONF_SYSFILES_DIR directory mapping the files to the
    corresponding file under the root directory, e.g.,
    "buildaudit/templates/sys/etc/nginx/nginx.conf" is
    used to create the system control file "/etc/nginx/nginx.conf".

    The control file templates are process by the standard Django template
    engine with all the YAMLCONF attributes available for substitution or
    control logic, e.g., instead of hardcoding the server name in a config
    file, the Django template subsitution "{{ SERVER_NAME }}" should be
    used.

    The list of attributes available via YAMLCONF can be listed using the
    "yclist" management command.
    """

    help = __doc__

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.root = None
        self.create = None

    def add_arguments(self, parser):
        """
        Add command line options.
        """
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--root', "-R",
            dest='root',
            default="",
            help='Root directory to install expanded files instead of "/"'
        )
        parser.add_argument(
            '--create', "-C",
            dest='create',
            default=False,
            action="store_true",
            help="Create the control files if they do not exist",
        )
        parser.add_argument(
            '--noop', "-N",
            dest='noop',
            default=False,
            action="store_true",
            help="No-op mode, print template output instead (debugging)"
        )

    def handle(self, *args, **options):
        """
        Implmentation of the command, simply walk the templates "sys" directory
        and use "render_to_string" using the YAMLCONF attributes to create
        the contents for the system control file.
        """
        super(Command, self).handle(*args, **options)
        sysfiles(options['create'], options['noop'], settings, options['root'])
