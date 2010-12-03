pycri
-----

Modular IRC-bot with support for live reloading of plugins. Support for TCP-
and SSL-connections.

Run the both with `python main.py <channel>`


Simple greeting plugin
----------------------

    from plugins import Plugin

    class Greeter(Plugin):
        def on_join(self, irc, prefix, params):
            nick, channel = prefix.split('!')[0], params[0]

            message = 'Welcome to {0}, {1}. Have a pleasant stay!'.format(
                channel, nick
            )

            irc.msg(channel, message)


That's it! Now either add the module to the PLUGINS-list in settings.py or
load the plugin using `!load <module>`.


Dependencies
------------

 - twisted
 - pyopenssl (if connecting over SSL)
