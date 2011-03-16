pycri
-----

Modular IRC-bot with support for live reloading of plugins. Support for TCP- and
SSL-connections.

Simple launcher
---------------

    import pycri.core
    application = pycri.core.run('#channel')

That's everything you need. Given that you have a settings.py-file with the
necessary variables (take a look at settings.py.example) you can now run the bot
with `python main.py`.


Simple greeting plugin
----------------------

    from pycri.plugins import Plugin, command

    class Greeter(Plugin):
        def on_join(self, irc, prefix, params):
            nick, channel = prefix.split('!')[0], params[0]

            message = u'Welcome to {0}, {1}. Have a pleasant stay!'.format(
                channel, nick
            )

            irc.msg(channel, message)

        @command(aliases=['gr'])
        def greet(self, nick):
            return 'Welcome {}'.format(nick)
            

That's it! Now either add the plugin to the PLUGINS-list in settings.py or load
the plugin using `!load <plugin>`. Remember that the plugins are loaded just as
any other module and must be on your python-path.

This plugin will greet all users joining the channel as well as adding a command
(accessible using !greet or the alias !gr) which takes one argument, the nick to
greet.


Dependencies
------------

 - twisted
 - pyopenssl (if connecting over SSL)
