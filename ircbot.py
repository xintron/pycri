import inspect, sys, traceback

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

            def callback(result):
                if result:
                    self.msg(channel, result)

            d = threads.deferToThread(method, *args)
            result = d.addCallback(callback)


    def handleCommand(self, command, prefix, params):
        for module, plugin in Plugin.library.iteritems():
            for cls in plugin.itervalues(): # Iterate over all classes for given plugin
                method = getattr(cls, 'on_' + command.lower(), None)

            try:
                if method:
                    threads.deferToThread(method, self, prefix, params)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout) # Print to console for debuging
                pass

        irc.IRCClient.handleCommand(self, command, prefix, params)

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
