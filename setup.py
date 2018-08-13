#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

import codecs
from os import path
from setuptools import setup

def readme():
    with codecs.open('README.md', 'r', 'utf-8') as f:
        return f.read()

def version():
    vers_path = path.join(
        path.dirname(__file__),
        "django_yamlconf",
        "VERSION"
    )
    with open(vers_path, "r") as fh:
        v_info = fh.readline()
    return ".".join(filter(lambda x: x != '', v_info.split(" ")))


setup(
    name='django-yamlconf',
    version=version(),
    author='Michael Rohan',
    author_email='mrohan@vmware.com',
    description='Define Django settings in local YAML (or JSON) files',
    long_description=readme(),
    license='BSD-2',
    platforms=['Any'],
    keywords=['django'],
    url='https://github.com/vmware/django-yamlconf',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Framework :: Django",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 2.0",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'Django>=1.7',
        'PyYAML>=3.10',
        'six>=1.10.0',
    ],
    packages=[
        'django_yamlconf',
        'django_yamlconf.templatetags',
        'django_yamlconf.management',
        'django_yamlconf.management.commands',
    ],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose', 'Jinja2'],
)
