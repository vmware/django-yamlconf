# -*- coding: utf-8 -*-
# Copyright © 2018-2019, VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause
"""
YAMLCONF
========

Handle YAML based Django settings: load Django settings from YAML files
based on a Django project name.  See the README.rst for additional
information.
"""
from __future__ import unicode_literals

import codecs
import copy
import getpass
import logging
import os
import platform
import sys
import textwrap
import traceback
import six

__all__ = [
    'add_attributes',
    'defined_attributes',
    'explain',
    'list_attrs',
    'load',
    'sysfiles',
]

logger = logging.getLogger(__name__)

_APPEND_MARKER = ":append"
_DOC_MARKER = ":doc"
_HIDE_MARKER = ":hide"
_PREPEND_MARKER = ":prepend"
_RAW_MARKER = ":raw"
_YAMLCONF_ATTRIBUTES = "_YAMLCONF_ATTRIBUTES"


def add_attributes(settings, attributes, source):
    """
    Add a set of name value pairs to the set of attributes, e.g.,
    attributes defined on the command line for management commands. Since
    this occurs after Django has loaded the settings, this function
    *does not*, in general, change behaviour of Django. It is used to
    add attribute definitions from management command lines. While this
    does not impact the behaviour of Django, it does make the attributes
    available for use in templates for the ``ycsysfiles`` command.

    :param settings: the Django settings module
    :param attributes: the dictionary of name/values pairs to add
    :param source: the name for the source (displayed by ``ycexplain``)
    :return: `None`

    """
    cur_attributes = get_cached_attributes(settings)
    for key, value in six.iteritems(attributes):
        set_attr_value(cur_attributes, settings, source, key, value)
    expand_attribute_refs(cur_attributes)
    inject_attr(cur_attributes, settings)


def add_attr_info(attributes, name, value, source="**INTERNAL**"):
    """
    Initialize a new attribute definition in the internal dict used to
    store the attribute and history of settings from various YAML files.
    """
    attributes[name] = {
        'value': value,
        'evalue': None,
        'source': source,
        'doc': [],
        'history': [],
        'hide': ('PASSWORD' in name),
    }


def extend_value(name, cur_value, value, append=True):
    """
    Append or prepend (depending on append argument)  the "value" to an
    existing value.
    """
    if not cur_value:
        return value
    elif isinstance(cur_value, (list, tuple)):
        result = copy.deepcopy(list(cur_value))
        if not isinstance(value, list):
            value = [value]
        if append:
            result.extend(value)
        else:
            result = value + result
        return result
    elif isinstance(cur_value, dict):
        result = copy.deepcopy(cur_value)
        if not isinstance(value, dict):
            logger.error(
                'Cannot append "%s" to "%s", "%s" is not a dict',
                value,
                name,
                type(value).__name__
            )
        else:
            for key in value.keys():
                result[key] = value[key]
        return result
    else:
        return [cur_value, value]


def bootstrap_attributes(base_dir):
    """
    Create the initial attribute set for YAMLCONF.  This set includes values
    that would not be available via other methods in a YAML file.  These
    attributes are available for attribute references in other values, e.g.,

        LOG_DIR: "{BASE_DIR}/log"
    """
    result = {}
    add_attr_info(result, 'TOP_DIR', os.path.dirname(base_dir))
    add_attr_info(result, 'BASE_DIR', base_dir)
    add_attr_info(result, 'VIRTUAL_ENV', os.environ.get("VIRTUAL_ENV", None))
    add_attr_info(result, 'USER', getpass.getuser())

    for name in ['machine', 'node', 'processor', 'release', 'system']:
        method = getattr(platform, name)
        add_attr_info(result, 'OS_{0}'.format(name.upper()), method())

    add_attr_info(result, 'PYTHON', {
        'MAJOR': sys.version_info.major,
        'MINOR': sys.version_info.minor,
        'MICRO': sys.version_info.micro,
        'RELEASELEVEL': sys.version_info.releaselevel,
        'SERIAL': sys.version_info.serial,
    })

    return result


def defined_attributes(settings=None, template_use=False):
    """
    Return a dictionary giving attribute names and associated values.
    This dictionary can be used as the variables when rendering templates.
    This is the set attributed used used as the variables when rendering
    templates for the ``ycsysfiles`` command.

    :param settings: the Django settings module (this is optional,
        defaults to the settings modules used when loading)
    :param template_use: If the the set of attributes return needs to be
        used to process a template, in the dictionary returned,
        attribute keys are added for dictionary parents e.g., "DATABASES", if
        "DATABASES.default..." is a YAMLCONF defined attribute.  The usage
        without this option support the `yclist` management command.
    :return: a dictionary giving attribute names and associated values.
    :rtype: dict
    """
    attributes = get_cached_attributes(settings)
    if not attributes:
        return {}
    result = {key: attributes[key]['evalue'] for key in attributes.keys()}
    # We are updating the result, avoid RunTimeError by creating a
    # temporary list for the set of keys in the iteration here
    for key in [k for k in result.keys()]:
        if '.' in key:
            base_key = key.split('.')[0]
            if base_key not in result:
                result[base_key] = getattr(settings, base_key)
    return result


def dirtree_find(filename, start_dir):
    """
    Iterator generating the instances of the given file name from the
    start_dir upto the root directory of the file system, e.g., the
    sequence of files generated might be

        /u/mrohan/clients/curwork/lib/python/xmpl.yaml
        /u/mrohan/clients/xmpl.yaml
        /u/mrohan/xmpl.yaml
    """
    curdir = start_dir or os.getcwd()
    done = False
    while not done:
        test_file = os.path.join(curdir, filename)
        if os.access(test_file, os.R_OK):
            yield test_file
        newdir = os.path.dirname(curdir)
        done = (newdir == curdir)
        curdir = newdir


def expand_attribute_refs(attributes):
    """
    Expand references to attributes in values, e.g., the set of definitions

        BASE_DIR: /var/osstp
        WEBAPPS_DIR: "{BASE_DIR}/webapps"

    would result in the definitions

        base_dir: /var/osstp
        webapps_dir: /var/osstp/webapps

    As can be seen from this example, attribute references use the Python
    dictionary formatting syntax to refer to other attributes.

    The routine "expand_attr_helper" is used to recurse over the attribute
    data.
    The set of expanded attribute values created is used to set the 'evalue's
    for each attribute.
    """
    values = expand_attr_helper(
        {key: attributes[key]['value'] for key in attributes.keys()}
    )
    for key, value in six.iteritems(values):
        attributes[key]['evalue'] = value


def expand_attr_helper(value, name="root", wrt=None):
    """
    Recurse over the attributes loaded expanding references.

    The name parameter is used to generate a path name to the attribute
    in case of errors, gives the user a little more information on which
    attribute has issues.

    The "wrt" (with respect to) is the set of attribute definitions.  This
    routine recursively expands included dictionaries and lists.  While
    the "value" to expand traverses down the full attribute set, the "wrt"
    value is always the top level attribute set.
    """
    wrt = wrt or value
    if isinstance(value, dict):
        for key in value.keys():
            if not value.get("{0}{1}".format(key, _RAW_MARKER), False):
                value[key] = expand_attr_helper(
                    value[key],
                    "{}[{}]".format(name, key),
                    wrt
                )
    elif isinstance(value, list):
        for i, _ in enumerate(value):
            value[i] = expand_attr_helper(
                value[i],
                "{}[{}]".format(name, i),
                wrt
            )
    elif isinstance(value, six.string_types):
        n_expand = 0
        done = False
        while not done:
            try:
                new_value = value.format(**wrt)
                done = (new_value == value)
                value = new_value
            except ValueError:
                logger.error('Invalid format value "%s" for "%s"', value, name)
                done = True
            except KeyError:
                logger.error('Undefined attribute "%s" in "%s"', value, name)
                done = True
            n_expand += 1
            if n_expand >= 10:
                logger.error('Recursive definition for "%s"', name)
                done = True
    return value


def explain(name, settings=None, stream=None):
    """
    Explain the source for an attribute definition including sources that
    were eclipsed by higher level YAML definition files.  If the attribute
    has associated documentation, it is also printed.

    This routine is only used by the YAMLCONF management command ``ycexplain``.

    :param name: the YAMLCONF controlled setting name
    :param settings: the Django settings module
    :param stream: the stream to write the explanation text (defaults to
        ``sys.stdout``)
    :return: `None`
    """
    stream = stream or sys.stdout
    attr_info = get_attr_info(name, settings=settings)
    if attr_info is None:
        stream.write("The setting \"{0}\" is not managed by YAMLCONF\n".format(
            name
        ))
        return
    stream.write("---------------------------\n")
    stream.write("{0} = \"{1}\" (via \"{2}\")\n".format(
        name,
        attr_info['value'],
        attr_info['source']
    ))
    if attr_info['value'] != attr_info['evalue']:
        stream.write("{0:{1}} = \"{2}\"\n".format(
            "",
            len(name),
            attr_info['evalue']
        ))
    stream.write("\n")
    documentation = attr_info['doc']
    if documentation:
        stream.write("Documentation:\n")
        for docstring in documentation:
            stream.write("{0}\n\n".format("\n".join(textwrap.wrap(
                docstring,
                width=65,
                initial_indent="    ",
                subsequent_indent="    "
            ))))
    if attr_info['history']:
        stream.write("Eclipsed values:\n")
        for value, source in attr_info['history']:
            stream.write("    \"{0}\" via \"{1}\"\n".format(value, source))


def get_attr_info(name, settings=None):
    """
    Get the information an attribute.
    """
    attributes = get_cached_attributes(settings)
    return attributes.get(name, None)


def get_settings_value(settings, name):
    """
    Get the value of an attribute defined in the settings module.  Dict
    access named attributes, are handled by digging into the dict in the
    settings file.  (Dict access names contain "." characteres, e.g.,
    "DATABASES.default.NAME"
    """
    components = name.split(".")
    result = getattr(settings, components[0], None)
    for component in components[1:]:
        if not isinstance(result, dict):
            logger.error('Not a dictionary: "%s" at "%s"', name, component)
            return None
        if component in result:
            result = result[component]
        else:
            return None
    return result


def get_attr_data(attributes, settings, name):
    """
    Return the dict describing an attribute value loaded from a YAML file.
    If this attribute has not already been seen, a new entry is created for
    it and returned.
    """
    if name not in attributes:
        add_attr_info(
            attributes,
            name,
            get_settings_value(settings, name),
            getattr(settings, "__name__", "settings")
        )
    return attributes[name]


def get_cached_attributes(settings=None):
    """
    When the YAML config files have been loaded, the data associated with
    the attributes defined is "cached" in the settings module via the attribute
    _YAMLCONF_ATTRIBUTES, this routine returns this cached data.

    This routine is used to support the management commands for YAMLCONF.
    """
    if settings is None:
        from django.conf import settings
    if not hasattr(settings, _YAMLCONF_ATTRIBUTES):
        logger.error("No YAMLCONF attributes defined")
        logger.error('"django_yamlconf.load" forgotten in the settings file?')
        setattr(settings, _YAMLCONF_ATTRIBUTES, {})
    return getattr(settings, _YAMLCONF_ATTRIBUTES)


def get_loader(syntax):
    """
    Return the "load" routine associated with the given file syntax, e.g., the
    "yaml.load" function.  The file syntax is assumed to name a module that
    has a "load" routine which parse an open file and returns dict/list of the
    file contents, e.g., "yaml.load", "json.load".
    """
    loader = None
    kwargs = {}
    try:
        module = __import__(syntax)
        loader = module.load
        if hasattr(module, "FullLoader"):
            kwargs = {'Loader': getattr(module, "FullLoader")}
    except ImportError as ex:
        logger.error('Unsupported YAMLCONF format "%s": %s', syntax, ex)
    except AttributeError as ex:
        logger.error('Loader "%s" has no "load" method: %s', syntax, ex)
    return loader, kwargs


def get_settings():
    """
    Return the settings module for the Django app that called the
    "yamlconf_load".  This should have been called from within the settings
    module so the stack trace back should give us the this module 3 up the
    call stack ("settings" + "get_settings" + "yamlconf_load").  The stack
    track is used to access the file name associate with the caller (0'th
    element) and from this the directory name is used as the Django application
    name.  Simply return "appname.settings" from the loaded modules in
    "sys.modules".
    """
    return sys.modules[
        "{0}.settings".format(os.path.basename(os.path.dirname(
            traceback.extract_stack(limit=3)[0][0]
        )))
    ]


def get_settings_dir(settings):
    """
    Return the directory containing the settings.py file.  This is simply
    the __file__ attribute of the settings module.  However, for testing
    purposes (and maybe it's useful in other contexts?) if the settings
    module is actually a class, return the __file__ value for the module
    defining the class.
    """
    path = os.getcwd()
    if hasattr(settings, "__file__"):
        path = settings.__file__
    elif hasattr(settings, "__module__"):
        path = sys.modules[settings.__module__].__file__
    return os.path.dirname(path)


def inject_attr(attributes, settings):
    """
    When the attributes have been loaded from various YAML files, this
    routine will "inject" the values into the "settings" module via
    the standard "setattr".   If the attribute names a dict element, i.e.,
    contains "." characters, the "injection" needs to traverse/create
    the supporting dictionaries in the settings file.

    To support the YAMLCONF management commands, the data accumlated on
    the attributes loaded is "cached" in the settings module via the
    attribute name _YAMLCONF_ATTRIBUTES.
    """
    setattr(settings, _YAMLCONF_ATTRIBUTES, attributes)
    for attr in attributes.keys():
        value = attributes[attr]['evalue']
        if '.' in attr:
            # Nested attribute (elements of a dict in the settings file)
            components = attr.split(".")
            target = getattr(settings, components[0], {})
            for key in components[1:-1]:
                if key not in target:
                    target[key] = {}
                target = target[key]
            if isinstance(target, dict):
                target[components[-1]] = value
        elif ':' not in attr:
            # Attributes with colons (:raw, :hide, etc) are not injected into
            # the settings module
            setattr(settings, attr, value)


def list_attrs(settings=None, stream=None):
    """
    Write a list of attributes managed by YAMLCONF to the given stream
    (defaults to ``sys.stdout``).
    Additional information can be printed using the ``explain`` routine.

    This routine is only used by the YAMLCONF management command ``yclist``.

    :param settings: the Django settings module
    :param stream: the stream to write the list text
    :return: `None`

    """
    stream = stream or sys.stdout
    attributes = get_cached_attributes(settings)
    if not attributes:
        stream.write("No YAMLCONF atttributes defined\n")
        return
    stream.write("Listing YAMLCONF managed attributes\n\n")
    # Determine the max attribute name length
    keylen = 0
    for name in attributes.keys():
        keylen = max(keylen, len(name))
    for name in sorted(attributes.keys()):
        stream.write("{0:<{1}}   {2}\n".format(
            name,
            keylen,
            attributes[name]['value']
        ))
    stream.write(
        "\nUse \"ycexplain\" for more information on individual attributes\n"
    )


def load(syntax="yaml", settings=None, base_dir=None, project=None):
    """
    Load the set of YAML files for a Django project.  The simplest usage is
    to call this at the end of a settings file.  In this context, no arguments
    are needed.

    :param syntax: The "syntax" parameter should name a Python module with
        a "load" method, e.g., the default is "yaml.load".  Other
        possibiliities could be "json" to use JSON formatted file or,
        even, "pickle" but that would be strange.  The "syntax" name is
        also used as the file extension for the YAMLCONF files.
    :param settings: The "settings" should be module containing the Django
        settings.  This is determined from the call stack if no module
        is given.
    :param base_dir: The "base_dir" defines the starting directory for
        YAMLCONF files and defaults to the directory containing the
        settings module.
    :param project: The "project" is the name of the Django project and
        defaults to the name of the directory containing the settings modules.
    :return: `None`
    """
    loader, loader_kwargs = get_loader(syntax)
    if loader is None:
        return
    settings = settings or get_settings()
    settings_dir = get_settings_dir(settings)
    base_dir = base_dir or os.path.dirname(settings_dir)
    project = project or os.path.basename(settings_dir)
    attr_filename = "{0}.{1}".format(project, syntax)
    attributes = bootstrap_attributes(base_dir)
    for filename in dirtree_find(attr_filename, settings_dir):
        load_conffile(attributes, settings, loader, loader_kwargs, filename)
    final_conf = os.environ.get("YAMLCONF_CONFFILE", None)
    if final_conf:
        load_conffile(attributes, settings, loader, loader_kwargs, final_conf)
    load_envdefs(attributes, settings)
    expand_attribute_refs(attributes)
    inject_attr(attributes, settings)


def load_conffile(attributes, settings, loader, loader_kwargs, filename):
    """
    Load an individual YAML file.  The data loaded is merged into the
    current set of attributes via the "set_attr_value" routine.
    """
    with codecs.open(filename, "r", encoding="utf-8") as defs:
        try:
            data = loader(defs, **loader_kwargs)
        except Exception as ex:
            logger.error('Failed to load "%s": %s', filename, ex)
            return
    if not isinstance(data, dict):
        logger.error(
            '"%s" did not define a dictionary: %s',
            filename,
            type(data)
        )
        return
    for name, value in six.iteritems(data):
        set_attr_value(attributes, settings, filename, name, value)


def load_envdefs(attributes, settings):
    """
    Load YAMLCONF attribute definitions from the environment.
    """
    for name, value in six.iteritems(os.environ):
        if name.startswith("YAMLCONF_"):
            set_attr_value(
                attributes,
                settings,
                "**ENVIRONMENT**",
                name.replace("YAMLCONF_", ""),
                value
            )


def set_attr_value(attributes, settings, filename, name, value):
    """
    Set an attribute value loaded from a YAML file.  If the attribute name
    ends with the _DOC_MARKED, the value is the documentation string for the
    attribute, set the 'doc' key instead.

    For regular attributes, the current value is stored in the history of
    loaded values (displayed via the "explain" routine and the "ycexplain"
    management command).
    """
    if name.endswith(_DOC_MARKER):
        name = name[:-len(_DOC_MARKER)]
        attr_data = get_attr_data(attributes, settings, name)
        attr_data['doc'].insert(0, value)
    elif name.endswith(_HIDE_MARKER):
        name = name[:-len(_HIDE_MARKER)]
        attr_data = get_attr_data(attributes, settings, name)
        attr_data['hide'] = True
    elif name.endswith(_APPEND_MARKER):
        name = name[:-len(_APPEND_MARKER)]
        attr_data = get_attr_data(attributes, settings, name)
        attr_data['history'].insert(
            0,
            (copy.deepcopy(attr_data['value']), attr_data['source'])
        )
        attr_data['source'] = filename
        attr_data['value'] = extend_value(name, attr_data['value'], value)
    elif name.endswith(_PREPEND_MARKER):
        name = name[:-len(_PREPEND_MARKER)]
        attr_data = get_attr_data(attributes, settings, name)
        attr_data['history'].insert(
            0,
            (copy.deepcopy(attr_data['value']), attr_data['source'])
        )
        attr_data['source'] = filename
        attr_data['value'] = extend_value(
            name,
            attr_data['value'],
            value,
            append=False
        )
    else:
        attr_data = get_attr_data(attributes, settings, name)
        attr_data['history'].insert(
            0,
            (copy.deepcopy(attr_data['value']), attr_data['source'])
        )
        attr_data['source'] = filename
        attr_data['value'] = value


def sf_init_file(create, noop, attrs, dst_filepath, src_filepath, render=None):
    """
    Initialize a system file based on a template under the "sys"
    template directory.
    """
    if not render:
        from django.template.loader import render_to_string
        render = render_to_string
    logger.debug(
        'YCSYSFILES: Rendering "%s" to "%s"',
        src_filepath,
        dst_filepath,
    )
    dst_filepath = os.path.normpath(dst_filepath.format(**attrs))
    contents = render(src_filepath, attrs)
    if noop:
        logger.info('Update: "%s"', dst_filepath)
        logger.info('-' * 50)
        logger.info("%s", contents)
        logger.info('-' * 50)
        return
    try:
        dirpath = os.path.dirname(dst_filepath)
        if create and not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        with codecs.open(dst_filepath, "wb", "utf-8") as dest_file:
            logger.info('Updating the system control file "%s"', dst_filepath)
            dest_file.write(contents)
    except (IOError, OSError):
        # Raise by either the makedirs or the open
        logger.debug(
            'Skipping non-writeable or missing system file: "%s"',
            dst_filepath
        )


def sysfiles(create, noop, settings, rootdir="", render=None):
    """
    Traverse the sys templates directory expanding files to the destination
    directory.

    :param create: the template files should be created, normally will only
        update files that already exist on the system and are writable.
    :param noop: no-op mode, print what would be done.
    :param settings: the Django settings module
    :param rootdir: the directory to create the system files, defaults to
        ``/``, i.e., the root file system.
    :param render: the rendering engine, if not given, defaults to Django's
        ``render_to_string``
    :return: `None`
    """
    attributes = defined_attributes(settings, template_use=True)
    templates_dir = attributes.get("YAMLCONF_SYSFILES_DIR", None)
    if templates_dir:
        td_len = len(templates_dir)
        for root, _, files in os.walk(templates_dir):
            dst_dir = "{0}{1}".format(rootdir, root[td_len:])
            for name in files:
                dst_path = os.path.join(dst_dir, name)
                src_path = os.path.join(root, name)
                sf_init_file(
                    create,
                    noop,
                    attributes,
                    dst_path,
                    src_path,
                    render
                )
    else:
        logger.error("No YAMLCONF_SYSFILES_DIR settings defined")


def _load_version():
    """
    Return the version information defined in the VERSION file.
    """
    with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r") as ver:
        v_info = ver.readline()
    major, minor, patch = filter(lambda x: x != '', v_info.strip().split(" "))
    return major, minor, patch


V_MAJOR, V_MINOR, V_PATCH = _load_version()
VERSION = "{0}.{1}.{2}".format(V_MAJOR, V_MINOR, V_PATCH)
