<!--
-*- coding: utf-8 -*-
    Copyright © 2018 VMware, Inc.  All rights reserved.
    SPDX-License-Identifier: BSD-2-Clause
-->

# django-yamlconf

`django_yamlconf` is part of VMware's support of open source development
and community.

Handle YAML based Django settings: load Django settings from YAML files
based on a Django project name.  The YAML files loaded start with a YAML
file in the directory containing the Django settings file and then loads
any other YAMLCONF files up the directory tree from the initial file.  Values
from files higher up the directory tree over-ride lower in the tree.  The
contents of the YAML file simply defines values that over-ride (or add to)
attributes of the standard Django settings file, e.g., for the project
"buildaudit", the settings.py file could contain::

    DEBUG = True

i.e., the value for development.  This can be redefined via a "buildaudit.yaml"
file using the definition::

    DEBUG: false

## License

`django-yamlconf` is release under the BSD-2 license, see the LICENSE file.

## Usage

The YAMLCONF definitions are added to the Django settings file by
including a call to the `load` function in the settings file.  This would
normally be towards the end of the settings file.  The simplest, and
likely normal usage is to call without arguments.  YAMLCONF will infer
the project information from the call stack.  For a standard Django
application structure, the settings file::

    myproject/myproject/settings.py

would contain the development oriented definitions, e.g., database
definitions for user and password for a development database.  The
settings file would then end with a call the the `load` function.
Additional definitions could be defined after the `load` function
to update conditional definitions, e.g., if `DEBUG` is enabled.

``` python
import django_yamlconf

DATABASES = {
    'default': {
        'NAME': 'example',
        'USER': 'example',
        'PASSWORD': 'example',
        'HOST': 'localhost',
        ...
    }
}
...

django_yamlconf.load()
```

The default format for attribute definitions is YAML.  The optional argument
`syntax` can be used to use a different format.  This argument should name a
Python module with a "load" method, e.g., the default, "yaml" support a "load"
method to load the definition from a file.  Other possibilities could be
"json" to use JSON formatted file or, even, "pickle" but that would be strange.
The "syntax" name is also used as the file extension for the YAMLCONF
files.

On a production server, for this example, a `myproject.yaml` would be put in
place containing the host name for the production database and the password
for the example user (assuming production is using the same database name
and username).  In this example, a random `pwgen` password is used::

``` yaml
DATABASES.default.PASSWORD: 'zibiemohjuD6foh0'
DATABASES.default.HOST: 'myproject-db.eng.vmware.com'
```

See the `load` function for more information on other optional
arguments.

## Management Commands

YAMLCONF includes three management commands (`django_yamlconf` needs to be
added to the `INSTALLED_APPS` to add these commands):

* ycexplain: explain where an attribute value was defined

* yclist: list the attribute values defined via YAMLCONF

* ycsysfiles: Create system control files based on attribute controlled
  template files

### `ycexplain` Command

This "ycexplain" gives information on the value defined by the set of YAML
files loaded for an application along with any documentation and information
on eclipsed attribute values lower in the directory tree structure.  For
example, for the DEBUG attribute::

```
    $ python manage.py ycexplain DEBUG
    ---------------------------
    DEBUG = "False" (via "/u/mrohan/clients/xmpl/buildaudit.yaml")

    Documentation:
        Enable or disable debugging functionality.  On the production
        server this attribute should be set to false

    Eclipsed values:
        "True" via "/u/mrohan/clients/xmpl/buildaudit/buildaudit.yaml"
        "True" via "buildaudit.settings"
```

### `yclist` Command

The "yclist" command simply lists the attributes defined via YAML files,
e.g.,::

```
    $ python manage.py yclist
    Listing YAMLCONF managed attributes

    ALLOWED_HOSTS                   ['localhost']
    BACKUP_CONFIG.directory         {BASE_DIR}/backup
    BASE_DIR                        /home/mrohan/clients/osstp-yc/webapps
    CONTROL_FILE                    {WEBAPPS_DIR}/osstpmgt.yaml
    DATABASES.default.CONN_MAX_AGE  600
    DATABASES.default.HOST          {DBHOST}
    DATABASES.default.NAME          {DBNAME}
    DATABASES.default.PASSWORD      {DBPASSWORD}
    DATABASES.default.USER          {DBUSER}
    DBHOST                          localhost
    DBNAME                          osstp
    DBPASSWORD                      A-Password
    DBUSER                          osstp
    INSTALL_DIR                     /var/oss/osstp
    MANAGE_PY                       {WEBAPPS_DIR}/manage.py
    OS_MACHINE                      x86_64
    OS_NODE                         mrohan-osstp-yc
    OS_PROCESSOR                    x86_64
    OS_RELEASE                      4.4.0-101-generic
    OS_SYSTEM                       Linux
    ROOT_URL                        https://{SERVER_NAME}
    SCM_ID                          v2017.07.13-103-gfac514b
    SERVER_NAME                     localhost
    TOP_DIR                         /home/mrohan/clients/osstp-yc
    USER                            mrohan
    VIRTUAL_ENV                     /home/mrohan/clients/venv
    WEBAPPS_DIR                     {BASE_DIR}
    YAMLCONF_SYSFILES_DIR           {BASE_DIR}/osstpmgt/templates/sys

    Use "ycexplain" for more information on individual attributes
```

### `ycsysfiles` Command

Coming soon.

## Support for Dictionaries

YAMLCONF uses the "." character to identify attributes defined as part of a
dictionary, e.g., the DATABASES attribute.  To set, e.g., the password for
a database connection::

``` yaml
    DATABASES.default.PASSWORD: some-secret-password
```

It is considered an error if dotted name refers to a settings attribute
that is not an dictionary, the setting is ignored by YAMLCONF.

The dotted notation should be used to update dictionaries already defined
in the settings file.  To add a new dictionary, a YAML dictionary definition
should be used, e.g.,::

``` yaml
    NEW_DICTIONARY:
        key1: value1
        key2: value2
```

## Attribute Substitution

Frequently, attributes values are defined in terms of other attribute values,
most commonly using the base directory to define other directories.  The
YAMLCONF allows other attributes to be referenced using the Python named
formatting syntax, e.g.,::

``` yaml
    LOG_DIR: "{BASE_DIR}/log"
```

Currently only attributes defined via YAML files can be used in this way.
To disable this on a per-attribute basis, the "`:raw`" qualifier should
be defined to modify the behaviour for attribute, e.g.,::

``` yaml
    LOGGING.formatters.simple.format: '%(asctime)s %(levelname)s %(message)s'
    LOGGING.formatters.simple.format:raw: True
```

## Hiding values

The YAMLCONF includes an experimental view to handle URLs to display
attributes (should only be used in a debugging context), e.g., adding
the URL definition to your applicaiton::

    url(r'^yamlconf/', include('django_yamlconf.urls')),

will display the YAMLCONF attributes.  By default, any attribute value with
the string "`PASSWORD`" in the name will have their values hidden in the
HTML displayed.  Other, sensitive, values can be explicitly hidden by defining
the qualifier attribute "`:hide`", e.g.,::

``` yaml
    APIKEY: 'my-api-key'
    APIKEY:hide: True
```

## Appending to Values

For list values, the qualifier attribute "`:add`" can be used to extend
the underlying definition, e.g., add another admin user, the following
definition can be used::

``` yaml
    ADMINS:add: 'someuser@vmware.com'
```

The value of "`:add`" qualified attribute can be either a single value,
as above, or a list of values.  When a list is given, the attribute is
extend with the extra values, e.g.,::

```
    ADMINS:add:
      - 'someuser1@vmware.com'
      - 'someuser2@vmware.com'
```

## Pre-defined Attributes

The YAMLCONF module predefines the following attributes which can be used,
along with other attributed defined, via attribute substitution:

`BASE_DIR`
    The directory containing the `setting.py` file

`PYTHON`
    This is a dictionary giving the major, minor, micro, releaselevel
    serial values for the Python interpretor

`OS_MACHINE`
    The value of the `platform.machine()` function, e.g., `x86_64`

`OS_NODE`
    The value of the `platform.node()` function, the system short name

`OS_PROCESSOR`
    The value of the `platform.machine()` function, e.g., `x86_64`

`OS_RELEASE`
    The value of the `platform.release()` function, e.g., `4.4.0-101-generic`

`OS_SYSTEM`
    The value of the `platform.system()` function, e.g., `Linux`

`TOP_DIR`
    The directory above BASE_DIR

`USER`
    The login name of the current user

`VIRTUAL_ENV`
    If run within a Python virtual environment, this attribute is defined
    to be the path to the environment, otherwise it has the value ``None``

## Attribute Documentation

Appending "`:doc`" to an attribute name in a YAML file defines a documentation
string for the attribute.  This should be used to give information on the
expected value for the attribute and how the value might differ on production,
beta and development servers, e.g., documentation for the DEBUG attribute
would be defined using the YAML::

``` yaml
    DEBUG:doc: |
        Enable or disable debugging functionality.  On the production server
        this attribute should be set to false
```

## Typical Structure

On a typical production system for the "buildaudit" app, a local
"buildaudit.yaml" would exist in, e.g., the "/var/www" directory.  This
would contain the production passwords, debug settings, etc.  Under this
directory, a "webapps" directory could contain another "buildaudit.yaml"
file possibly generated by a build process which could define attributes
identifying the build, the Git Hash for the code, build time, etc. Finally,
a "buildaudit.yaml" file co-located with the settings.py file giving the
base attributes and their documentation strings::

    +- /var/www
        +- buildaudit.yaml
        +- webapps
           +- buildaudit.yaml
           +- buildaudit
               +- buildaudit.yaml
               +- settings.py

## URL Available

The package includes support to display the values defined via YAMLCONF
files:

![Attributes Index Page](images/yamlconf-list.png "YAMLCONF Index Page")


## Public Methods

The primary public method is the `load` method which loads the attribute
definitions from YAML file located in the directory tree.  Other methods
are exported, and are documented here, but it is expected that these
methods are only used by the management commands.

### `add_attributes` Function

``` python
add_attributes(settings, attributes, source)
```

Parameters:
* `settings`, the Django settings module
* `attributes`, the dictionary of name/values pairs to add
* `source`, the name for the source (displayed by `ycexplain`)

Add a set of name value pairs to the set of attributes, e.g., attributes
defined on the command line for management commands.  Since this occurs
after Django has loaded the settings, this function _does not_, in general,
change behaviour of Django.  It is used to add attribute definitions from
management command lines.  While this does not impact the behaviour of
Django, it does make the attributes available for use in templates for
the `ycsysfiles` command.

### `defined_attributes` Function

``` python
defined_attributes(settings)
```
Return a dictionary giving attribute names and associated values.
This dictionary is used as the variables when rendering templates
for the `ycsysfiles` command.

### `explain` Function

``` python
explain(name, settings, stream=sys.stdout)
```

Explain the source for an attribute definition including sources that
were eclipsed by higher level YAML definition files.  If the attribute
has associated documentation, it is also printed.

This routine is only used by the YAMLCONF management commands.

### `list_attrs` Function
### `load` Function
### `sysfiles` Function

The public methods are normally expected to used only by th

## Limitations

Some of the current limitations for this implementation are:

* Currently cannot substitute list values, e.g.,::

``` yaml
    ADMINS:
      - jsmith
      - auser
    MANAGER: "{ADMINS}"
```

* The pre-defined attributes should also include the host IP address

These might be addressed if the need arises.

## Examples

The examples are based on the `polls` example from the
[Django Project](https://www.djangoproject.com/) web site.  There are two
flavors of this example:

1. Under Django version 1.11
2. Under Django version 2.0

## Django 1.11 Example

This is the `polls` example from the
[Django Project](https://www.djangoproject.com/) web site.  There is
little usage of custom settings for this example, however, when deployed
under, e.g., Apache, settings can be used to control the Apache control
file used and

## Releases & Major Branches

### Version 1.0.0

* Initial release (tagged with `v1.0.0`)

## Contributing

The `django-yamlconf` project team welcomes contributions from the
community. If you wish to contribute code and you have not signed our
contributor license agreement (CLA), our bot will update the issue
when you open a Pull Request. For any questions about the CLA process,
please refer to our [FAQ](https://cla.vmware.com/faq). For more detailed
information, refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## Authors

Created and maintained by Michael Rohan <mrohan@vmware.com>
