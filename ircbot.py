import inspect

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

from plugins import Plugin
import settings


class IRCBot(irc.IRCClient):

    nickname = settings.NICKNAME
    realname = settings.REALNAME

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
            args = msg[1:].split(' ')
            cmd = args.pop(0)

            # Search plugins for commands
            method = Plugin.commands.get(cmd, None)

            if not method:
                return

            # Validate arguments
            argspec = inspect.getargspec(method)

            given_argument_count = len(args)
            required_argument_count = len(argspec.args) - 1

            if argspec.defaults:
                required_argument_count -= len(argspec.defaults)

            if given_argument_count < required_argument_count:
                msg = '{0}{1} requires {2} argument{3} ({4}), but {5} was given.'.format(
                    self.factory.prefix,
                    cmd,
                    required_argument_count,
                    's' if required_argument_count != 1 else '',
                    ', '.join(argspec.args[1:]),
                    given_argument_count
                )

                self.msg(channel, msg)

                return

            result = method(*args)

            if result:
                self.msg(channel, result)


    def handleCommand(self, command, prefix, params):
        for module, plugin in Plugin.library.iteritems():
            method = getattr(plugin, 'on_' + command.lower(), None)

            try:
                if method:
                    method(self, prefix, params)
            except:
                pass

        irc.IRCClient.handleCommand(self, command, prefix, params)


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
