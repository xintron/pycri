# -*- coding: utf-8 -*-
"""
    pycri.globals
    -------------

    Defiens the global object that contains the current application instance.

    :copyright: (c) 2012 by Marcus Carlsson
    :license: BSD, see LICENSE for more details
"""


from twisted.internet import reactor

def gapp():
    if not hasattr(reactor, 'app'):
        reactor.app = None
    return reactor.app

g = gapp()
del gapp
