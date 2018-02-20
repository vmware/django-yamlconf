# -*- coding: utf-8 -*-
# Copyright © 2018 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

"""
URL mappings to display the YAMLCONF settings.  This should only be used
for admin users.  The views are protected via

    @login_required(login_url='/admin/login/')

If you have a special environment, you might need to adjust this.
"""

from django.conf.urls import url
from django_yamlconf import views

app_name = 'django_yamlconf'
urlpatterns = [
    url("^$", views.index, name='index'),
    url("^(?P<name>.+)/$", views.attr_info, name='attr'),
]
