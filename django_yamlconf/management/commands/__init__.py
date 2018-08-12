# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
Django YAMLCONF management commands.
"""
from __future__ import unicode_literals

import importlib
import logging
import six

from django.conf import settings
from django.core.management.base import BaseCommand

import django_yamlconf

logger = logging.getLogger(__name__)


def add_cmd_attrs(defines, methods):
    """
    Add attributes defined on the command line, via name=value of an
    application method, to the set of attributes available in templates.
    """
    django_yamlconf.add_attributes(
        settings,
        get_methods(methods),
        "**GENERATED**"
    )
    django_yamlconf.add_attributes(
        settings,
        get_defines(defines),
        "**CMDLINE**"
    )


def get_defines(defines):
    """
    Return a dictionary of command line defined attribute values, e.g.,

        -D A=B

    returns

        {'A': 'B'}
    """
    result = {}
    for key_value in defines or []:
        try:
            key, value = key_value.split("=", 1)
            result[key] = value
            logger.debug('Adding "%s" => "%s"', key, value)
        except ValueError:
            logger.warning(
                'Invalid command line attribute definition "%s"',
                key_value
            )
    return result


def get_methods(methods):
    """
    Return a dictionary of attributes defined via application methods.
    """
    result = {}
    for method in methods or []:
        try:
            mod_name, func_name = method.rsplit('.', 1)
            func = getattr(
                importlib.import_module(mod_name),
                func_name
            )
            method_attrs = func()
            for key, value in six.iteritems(method_attrs):
                result[key] = value
        except ValueError:
            logger.warning('"%s" does not name a packaged method', method)
        except ImportError as ex:
            logger.warning('Method module "%s" failure: %s', mod_name, ex)
        except TypeError:
            logger.warning('"%s" did not return a dictionary', method)
        except AttributeError as ex:
            logger.warning(
                'Method module "%s" has no "%s": %s',
                mod_name, func_name, ex
            )
    return result


class YCBaseCommand(BaseCommand):
    """
    Common funcitonality for the YAMLCONF management commands: common
    options and handling.
    """

    def __init__(self, *args, **kwargs):
        super(YCBaseCommand, self).__init__(*args, **kwargs)
        self.verbosity = 1

    def add_arguments(self, parser):
        """
        Add command line options.
        """
        parser.add_argument(
            '--define', '-D',
            dest='defines',
            action='append',
            help="Additional command line defined attributes (name=value)"
        )
        parser.add_argument(
            '--attribute', '-A',
            dest='attributes',
            action='append',
            help="Method returning dict of addtional key/value pairs",
        )

    def handle(self, *args, **options):
        """
        Implmentation of the command, simply walk the templates "sys" directory
        and use "render_to_string" using the YAMLCONF attributes to create
        the contents for the system control file.
        """
        self.verbosity = options['verbosity']
        attributes = getattr(settings, 'YAMLCONF_ATTRIBUTE_FUNCTIONS', [])
        if options['attributes']:
            attributes.extend(options['attributes'])
        add_cmd_attrs(options['defines'], attributes)
