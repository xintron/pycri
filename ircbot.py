# -*- coding: utf-8 -*-

import sys, os
from copy import copy

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

from utils.plugin_handler import new_plugins, main_plugin
from utils.base import _map as namespace
import settings

class IRCBot(irc.IRCClient):

    nickname = settings.NICKNAME
    realname = settings.REALNAME

    def signedOn(self):
        """Connection to the server made. Join channels."""

        self.join(self.factory.channel)

    def userJoined(self, user, channel):
        self._handle_hooks('on_user_joined', user, channel)

    def privmsg(self, user, channel, msg):
        """Handle incomming messages. If starting with a prefix, check for matching command and run!"""

        self._handle_hooks('on_privmsg', user, channel, msg)

        # If prefixed, look for proper command and run plugin
        if msg.startswith(self.factory.prefix):
            args = msg[1:].split(' ')
            cmd = args.pop(0)

            # This is a special command to reload all plugins
            if cmd == 'reload':
                self.factory._load_plugin()

            elif cmd in self.factory._commands:
                try:
                    plugin, trigger = self.factory._commands[cmd]
                    plugin.__dict__[trigger](plugin, self, user, channel, args)
                except Exception, e:
                    print e


    def _handle_hooks(self, hook, *args):
        """Handle hooks. Search plugins for hooks and run all related plugins"""
        if hook in self.factory._hooks:
            for plugin in self.factory._hooks[hook]:
                try:
                    plugin.__dict__[hook](plugin, self, *args)
                except Exception, e:
                    print e


class IRCBotFactory(protocol.ClientFactory):

    protocol = IRCBot

    def __init__(self, channel, prefix):
        self.channel = channel
        self.prefix = prefix
        self.plugin = main_plugin
        self.ns = new_plugins

        # Do not reload plugins the first run
        self._plugin_loaded = False

    def startFactory(self):
        self._load_plugin()

        protocol.ClientFactory.startFactory(self)

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()


    def _load_plugin(self, load_plugin = None):
        """Load plugins"""
        if load_plugin:
            load_plugin = '{}.{}'.format(self.plugin.__name__, load_plugin)
            __import__(load_plugin)
            load_plugin = sys.modules[load_plugin]
            self.ns.append(load_plugin)
        else:
            if self._plugin_loaded:
                # Empty namespace map over classes
                namespace.clear()

                for plugin in self.ns:
                    try:
                        reload(plugin)
                    except:
                        print 'error when reloading plugin', plugin.__name__, sys.exc_info()
                print 'Reload done'
            else:
                self._plugin_loaded = True
        self._load_aliases(load_plugin)


    def _load_aliases(self, load_plugin):
        """Reload aliases for a specific plugin or all plugins"""

        def _import_aliases(plugin):
            if callable(plugin) and hasattr(plugin, 'triggers') and plugin.triggers:
                for trigger, aliases in plugin.triggers.items():
                    for alias in aliases:
                        assert alias not in self._commands, 'Command redefination ({})'.format(alias)
                        self._commands[alias] = (plugin, trigger)
            return

        def _import_hooks(plugin):
            for key in plugin.__dict__.keys():
                if key.startswith('on_'):
                    if key in self._hooks:
                        self._hooks[key].append(plugin)
                    else:
                        self._hooks[key] = [plugin]

        self._commands = {}
        self._hooks = {}
        for name, plugin in namespace.items():
            _import_aliases(plugin)
            _import_hooks(plugin)


