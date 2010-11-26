# -*- coding: utf-8 -*-

"""Module with classes.

"""

__author__ = 'Marcus Carlsson <carlsson.marcus@gmail.com>'
_map = {}

class PluginInitializer(type):
    """Meta-class for setting up plugin classes.
    
    Keeps track of hooks and commands so that the appropriate
    class for a certain hook/command can be fetched
    
    """

    def __new__(cls, name, base, dct):
        t = type.__new__(cls, name, base, dct)

        if '_plugin_name' not in dct:
            return t

        assert dct['_plugin_name'] not in _map, (
            '{} redefines plugin_name ({})'.format(name, _map[dct['_plugin_name']])
        )

        _map[dct['_plugin_name']] = t
        return t

        

class Plugin(object):
    """Plugin base-class
    
    """
    __metaclass__ = PluginInitializer

    def __init__(self):
        pass

    def on_join(self):
        pass

    def on_privmsg(self):
        pass


class Command(Plugin):
    triggers = []
