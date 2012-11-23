# -*- coding: utf-8 -*-
"""
    pycri.ext
    =========

    Redirect imports for extensions. When a user does ``from pycri.ext.foo
    import bar`` it will attempt to import ``from pycri_foo import bar``.

    :copyright: (c) 2012 Marcus Carlsson
    :license: BSD, see LICENSE for more details.
"""

def setup():
    from ..exthook import ExtensionImporter
    target = ExtensionImporter(__name__)
    target.install()

setup()
del setup
