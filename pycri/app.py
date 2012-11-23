# -*- coding: utf-8 -*-
"""
pycri.app
=====

This module implements the central IRC application object.

:copyright: (c) 2012 by Marcus Carlsson
:license: BSD, see LICENSE for more details
"""

import inspect
import socket
import sys
import logging

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, threads
from twisted.python import log

from pycri.plugins import IRCObject
from pycri.utils.encoding import smart_str

try:
    import settings
except:
    print 'You have to create a settings-file. Please take a look at the example settings.py shipped with this package.'
    sys.exit(1)

class Pycri(object):
    """The Pycri object implements a application and acts as the central
    object. Once it is created it will act as a central registry for the
    connection(s), configuration and much more.

    The first parameter should be the name of the module or package of the
    application. The name of the application is used to resolve resources from
    inside the module or the folder the module is contained in. Usually you
    want to create a :class:`Pycri` instance in your main module or in the
    `__init__.py` file of your package like so::

        from pycri import Pycri
        app = Pycri(__name__)

    :param import_name: the name of the application package
    """

    def __init__(self, import_name):
        reactor.app = self
        self.import_name = import_name
        self._logger = None
        self.logger_name = import_name

    @property
    def logger(self):
        """A :class:`logging.Logger` object for the root application."""
        if self._logger and self._logger.name == self.logger_name:
            return self._logger
        self._logger = logging.getLogger(self.logger_name)
        return self._logger

    def getLogger(self, name):
        """Convenient method for extensions to fetch a :class:`logging.Logger`
        object for their extension instead of using the root application
        name."""
        return logging.getLogger(name)


    def run(self, channel):
        """Method for starting the application and opening the defined
        connections."""
        socket.setdefaulttimeout(15)

        reactor.app = self

        logging.basicConfig(level=logging.DEBUG, 
            format="[%(asctime)s] %(name)s - %(levelname)s %(msg)s")
        observer = log.PythonLoggingObserver()
        observer.start()

        self.factory = IRCBotFactory(channel, '!')

        self.logger.info('Opening connection')
        if settings.NETWORK_USE_SSL:
            try:
                from twisted.internet import ssl
            except ImportError:
                try:
                    from OpenSSL import ssl
                except ImportError:
                    print 'Please install the OpenSSL-package (pyOpenSSL) if \
                            you need SSL-connections'
                    sys.exit(1)
            reactor.connectSSL(settings.NETWORK_ADDR, settings.NETWORK_PORT,
                    self.factory, ssl.ClientContextFactory())
        else:
            reactor.connectTCP(settings.NETWORK_ADDR, settings.NETWORK_PORT,
                    self.factory)

        reactor.run()

class IRCBot(irc.IRCClient):

    nickname = smart_str(settings.NICKNAME)
    realname = smart_str(settings.REALNAME)
    username = smart_str(settings.USERNAME)
    password = smart_str(settings.PASSWORD)

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
            method = IRCObject.commands.get(cmd, None)

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
            def callback(result):
                if result:
                    self.msg(channel, result)
            d = threads.deferToThread(method, *args)
            d.addCallback(callback)


    def handleCommand(self, command, prefix, params):
        for module, plugin in IRCObject.library.iteritems():
            for cls in plugin.itervalues(): # Iterate over all classes for given plugin
                method = getattr(cls, 'on_' + command.lower(), None)
                if method:
                    try:
                        reactor.callFromThread(method, self, prefix, params)
                    except: # TODO: Log exceptions for debugging but for now just let the exceptions pass so that the bot doesn't reconnect
                        pass

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
            IRCObject.load(plugin)

        protocol.ClientFactory.startFactory(self)

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()


