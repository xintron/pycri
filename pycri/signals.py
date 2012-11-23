# -*- coding: utf-8 -*-
"""
    pycri.signals
    -----

    Signals implementation based on blinker if available.

    :copyright: (c) 2012 by Marcus Carlsson
    :license: BSD, see LICENSE for more details
"""
signals_available = False
try:
    from blinker import Namespace
    signals_available = True
except ImportError:
    raise RuntimeError('Signalling is unavailable because blinker is not \
        installed')

_signals = Namespace()

extension_teardown = _signals.signal('extension-teardown')
extension_setup = _signals.signal('extension-setup')
