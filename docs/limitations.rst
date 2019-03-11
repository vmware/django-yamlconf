.. -*- coding: utf-8 -*-
   Copyright © 2019, VMware, Inc.  All rights reserved.
   SPDX-License-Identifier: BSD-2-Clause

Limitations
-----------

Some of the current limitations for this implementation are:

-  Currently cannot substitute list values, e.g.,:

.. code:: yaml

        ADMINS:
          - jsmith
          - auser
        MANAGER: "{ADMINS}"

-  The pre-defined attributes should also include the host IP address

These might be addressed if the need arises.
