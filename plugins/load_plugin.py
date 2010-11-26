from utils import base

class LoadPlugin(base.Command):

    _plugin_name = 'loadplugin'

    triggers = {
        'load': ['loadplugin'],
    }

    def load(self, irc, user, channel, args = None): 
        if len(args) == 1:
            irc.factory._load_plugin(args[0])
            irc.msg(channel, 'loaded plugin ({})'.format(args[0]))
