# -*- coding: utf-8 -*-

import sys, os
from copy import copy

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, threads

from plugins import Plugin
import settings

class IRCBot(irc.IRCClient):

    nickname = settings.NICKNAME
    realname = settings.REALNAME

    def signedOn(self):
        """Connection to the server made. Join channels."""
        self.join(self.factory.channel)

    def privmsg(self, user, channel, msg):
        """Handle incomming messages.
        
        If starting with a prefix, check for matching command and run!
        """

        # If prefixed, look for proper command and run plugin
        if msg.startswith(self.factory.prefix):
            args = msg[1:].split(' ')
            cmd = args.pop(0)

            # Search plugins for commands
            module_method = Plugin.commands.get(cmd, None)

            if not module_method:
                return

            module, method = module_method.split('.')

            method = getattr(Plugin.library[module], method, None)

            if method and callable(method):
                result = method(*args)

                if result:
                    self.say(channel, result)


    def handleCommand(self, command, prefix, params):
        for module, plugin in Plugin.library.iteritems():
            method = getattr(plugin, 'on_' + command.lower(), None)

            try:
                if method:
                    method(prefix, params)
            except:
                pass

        irc.IRCClient.handleCommand(self, command, prefix, params)


class IRCBotFactory(protocol.ClientFactory):

    protocol = IRCBot

    def __init__(self, channel, prefix):
        self.channel = channel
        self.prefix = prefix

    def startFactory(self):
        Plugin.autoload()

        protocol.ClientFactory.startFactory(self)

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()
