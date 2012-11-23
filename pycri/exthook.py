# -*- coding: utf-8 -*-
"""
    pycri.ext
    =========

    Redirect imports for extensions. When a user does ``from pycri.ext.foo
    import bar`` it will attempt to import ``from pycri_foo import bar``.

    :copyright: (c) 2012 Marcus Carlsson
    :license: BSD, see LICENSE for more details.
"""
import sys

class ExtensionImporter(object):
    """This importer redirects imports from this submodule to other
    locations."""

    module = "pycri_{}"
    def __init__(self, wrapper_module):
        self.wrapper_module = wrapper_module
        self.prefix = wrapper_module + '.'
        self.prefix_cutoff = wrapper_module.count('.') + 1

    def __eq__(self, other):
        return self.__class__.__module__ == other.__class__.module__ and \
                self.__class__.__name__ == other.__class__.__name__ and \
                self.module == other.module and \
                self.wrapper_module == other.wrapper_module

    def __ne__(self, other):
        return not self.__eq__(other)

    def install(self):
        sys.meta_path[:] = [x for x in sys.meta_path if x != self] + [self]

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.prefix):
            return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        modname = fullname.split('.', self.prefix_cutoff)[self.prefix_cutoff]
        realname = self.module.format(modname)
        __import__(realname)
        module = sys.modules[fullname] = sys.modules[realname]
        if '.' not in modname:
            setattr(sys.modules[self.wrapper_module], modname, module)
        return module
