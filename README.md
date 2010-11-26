pycri
-----
Modular IRC-bot with support for live reloading of plugins. Support for TCP- and SSL-connections.

Run the both with `python main.py <channel>`


Simple greeting plugin
----------------------
    from utils import base

    class Greeter(base.Plugin):
        _plugin_name = 'channel_greeter' # Plugin name is needed for the module to be loaded at all

        def on_user_joined(self, user, channel): # The `on_user_joined` hook sends with the class itself, the bot-instance and the user joined as well as the channel for the event
            irc.msg(channel, 'Welcome to {}, {}. Have a pleasant stay!'.format(channel, user.split('!')[0))

That's it! Now either add the module to the list in plugins.\__all\__ (plugins/\__init\__.py) or load the plugin using `!loadplugin <module>`


Dependencies
------------
 - twisted
 - pyopenssl (if connecting over SSL)
