# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Copyright (c) 2010-2011, Marcus Carlsson <carlsson.marcus@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.
    * Neither the name of the author nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import inspect, sys, traceback, socket

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

from pycri.plugins import Plugin
from pycri.utils.encoding import smart_str

try:
    import settings
except:
    print 'You have to create a settings-file. Please take a look at the example settings.py shipped with this package.'
    quit()

class IRCBot(irc.IRCClient):

    nickname = smart_str(settings.NICKNAME)
    realname = smart_str(settings.REALNAME)
    username = smart_str(settings.USERNAME)

    def signedOn(self):
        """Connection to the server made. Join channels."""
        self.join(self.factory.channel)

    def privmsg(self, user, channel, msg):
        """
        Handle incoming privmsgs.
        
        If starting with a prefix, check for matching command and run!
        """

        # If prefixed, look for proper command and run plugin
        if msg.startswith(self.factory.prefix):
            args = msg[1:].strip().split(' ')
            cmd = args.pop(0)

            # Search plugins for commands
            method = Plugin.commands.get(cmd, None)

            if not method:
                return

            # Validate arguments
            argspec = inspect.getargspec(method)

            given_argument_count = len(args)
            required_argument_count = required_static_argument_count = len(argspec.args) - 1

            if argspec.defaults:
                required_static_argument_count -= len(argspec.defaults)

            if given_argument_count < required_static_argument_count or (given_argument_count > required_argument_count and not argspec.varargs):
                diff = required_argument_count + 1
                if argspec.defaults:
                    diff -= len(argspec.defaults)
                    defaults = ['{}={}'.format(x, argspec.defaults[argspec.args.index(x)-diff]) for x in argspec.args[diff:]]

                msg = '{0}{1} requires {2} argument{3}{4} ({5}{6}), but {7} was given.'.format(
                    self.factory.prefix,
                    cmd,
                    required_static_argument_count,
                    's' if required_static_argument_count != 1 else '',
                    ' ({} optional)'.format(len(argspec.defaults)) if argspec.defaults else '',
                    ', '.join(argspec.args[1:diff]), # Break if there are default values and print them next
                    ', [{}]'.format(', '.join(defaults)) if argspec.defaults else '',
                    given_argument_count
                )

                self.msg(channel, msg)

                return
            result = method(*args)
            if result:
                self.msg(channel, result)


    def handleCommand(self, command, prefix, params):
        for module, plugin in Plugin.library.iteritems():
            for cls in plugin.itervalues(): # Iterate over all classes for given plugin
                method = getattr(cls, 'on_' + command.lower(), None)
                if method:
                    method(self, prefix, params)

        irc.IRCClient.handleCommand(self, command, prefix, params)

    def msg(self, channel, msg):
        msg = smart_str(msg)
        irc.IRCClient.msg(self, channel, msg)

    def _print_error(self, msg):
        print msg

    def _print_result(self, msg):
        if msg:
            print msg


class IRCBotFactory(protocol.ClientFactory):

    protocol = IRCBot

    def __init__(self, channel, prefix):
        self.channel = channel
        self.prefix = prefix

    def startFactory(self):
        for plugin in settings.PLUGINS:
            Plugin.load(plugin)

        protocol.ClientFactory.startFactory(self)

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()


def run(channel):
    socket.setdefaulttimeout(15)

    factory = IRCBotFactory(channel, '!')

    if settings.NETWORK_USE_SSL:
        try:
            from twisted.internet import ssl
        except ImportError:
            try:
                from OpenSSL import ssl
            except ImportError:
                print 'Please install the OpenSSL-package (pyOpenSSL) if you need SSL-connections'
                quit()
        reactor.connectSSL(settings.NETWORK_ADDR, settings.NETWORK_PORT, factory, ssl.ClientContextFactory())
    else:
        reactor.connectTCP(settings.NETWORK_ADDR, settings.NETWORK_PORT, factory)

    reactor.run()
