pycri
-----

Modular IRC-bot with support for live reloading of plugins. Support for TCP-
and SSL-connections.

Run the both with `python main.py <channel>`


Simple greeting plugin
----------------------

    from plugins import Plugin, command

    class Greeter(Plugin):
        def on_join(self, irc, prefix, params):
            nick, channel = prefix.split('!')[0], params[0]

            message = 'Welcome to {0}, {1}. Have a pleasant stay!'.format(
                channel, nick
            )

            irc.msg(channel, message)

        @command(aliases=['gr'])
        def greet(self, nick):
            return 'Welcome {}'.format(nick)
            

That's it! Now either add the plugin to the PLUGINS-list in settings.py or
load the plugin using `!load <plugin>`.

This plugin will greet all users joining the channel as well as adding a
command (accessible using !greet or the alias !gr) which takes one argument,
the nick to greet.


Dependencies
------------

 - twisted
 - pyopenssl (if connecting over SSL)
