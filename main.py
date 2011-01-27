# -*- coding: utf-8 -*-
"""
Copyright (c) 2010, Marcus Carlsson <carlsson.marcus@gmail.com>
All rights reserved.

You may redistribute and use -
as source or binary, as you choose,
and with some changes or without -
this software; let there be no doubt.
But you must meet conditions three,
if in compliance you wish to be.

The first is obvious, of course -
To keep this text within the source.
The second is for binaries
Place in the docs a copy, please.
A moral lesson from this ode - 
Don't strip the copyright on code.

The third applies when you promote:
You must not take, from us who wrote,
our names and make it seem as true
we like or love your version too.
(Unless, of course, you contact us
And get our written assensus.)

One final point to be laid out
(You must forgive my need to shout):
THERE IS NO WARRANTY FOR THIS
WHATEVER THING MAY GO AMISS.
EXPRESS, IMPLIED, IT'S ALL THE SAME -
RESPONSIBILITY DISCLAIMED.

WE ARE NOT LIABLE FOR LOSS
NO MATTER HOW INCURRED THE COST
THE TYPE OR STYLE OF DAMAGE DONE
OR CLEVER LEGAL THEORY SPUN.
THIS EVEN STAYS THE CASE IF YOU
INFORM US WHAT YOU PLAN TO DO.

When all is told, we sum up thus -
Do what you like, just don't sue us.

"""
#!/usr/bin/env python

__author__ = 'Marcus Carlsson <carlsson.marcus@gmail.com>'
__contributor__ = 'Marcus Fredriksson <drmegahertz@gmail.com>' # Rewrote the plugin handling system
__version__ = 0.2.1


import sys, socket

from twisted.internet import reactor

from ircbot import IRCBotFactory
import settings


if __name__ == '__main__':
    socket.setdefaulttimeout(15)

    factory = IRCBotFactory(sys.argv[1], '!')

    if settings.NETWORK_USE_SSL:
        from twisted.internet import ssl
        reactor.connectSSL(settings.NETWORK_ADDR, settings.NETWORK_PORT, factory, ssl.ClientContextFactory())
    else:
        reactor.connectTCP(settings.NETWORK_ADDR, settings.NETWORK_PORT, factory)

    reactor.run()
