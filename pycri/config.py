# -*- coding: utf-8 -*-
"""
    pycri.config
    ------------

    Implements the configuration object.

    :copyright: (c) 2012 by Marcus Carlsson
    :license: BSD, see LICENSE for more details
"""
import imp
import os

class Config(dict):
    """Works like a dict but provides method for reading settings from
    python-modules."""

    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = os.path.dirname(os.path.realpath(__file__))

    def from_pyfile(self, filename):
        """Updates the values from the given python file."""
        c = imp.new_module('config')
        c.__file__ = filename
        try:
            execfile(filename, c.__dict__)
        except IOError, e:
            e.strerror = \
                'Unable to load configuration file ({})'.format(e.strerror)
            raise
        self.from_object(c)
        return True

    def from_object(self, obj):
        """Updates the config-values from the gven object. Only uppercase
        variables will be loaded."""
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
