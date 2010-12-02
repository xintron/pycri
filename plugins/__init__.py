import imp
import inspect

import settings


class PluginLibrary(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'library'):
            cls.library = {}
        else:
            cls.library[cls.__module__] = cls()

        type.__init__(cls, name, bases, attrs)


class Plugin(object):
    __metaclass__ = PluginLibrary

    commands = {}

    @classmethod
    def load(cls, name):
        fp, pathname, description = imp.find_module(name, ['plugins'])

        try:
            imp.load_module(name, fp, pathname, description)

            # Collect the methods that's marked as commands
            for name, obj in inspect.getmembers(cls.library[name]):
                if not name.startswith('_') and inspect.ismethod(obj):
                    if hasattr(obj, 'command'):
                        commands = [obj.command] + obj.aliases

                        for command in commands:
                            cls.commands[command] = obj

        finally:
            if fp:
                fp.close()

    @classmethod
    def unload(cls, name):
        plugin = cls.library[name]

        commands_to_unload = []
        for command, method in cls.commands.iteritems():
            if method.im_self is plugin:
                commands_to_unload.append(command)

        for command in commands_to_unload:
            del cls.commands[command]

        del cls.library[name]


    @classmethod
    def reload(cls, name):
        cls.unload(name)
        cls.load(name)

def command(func=None, name='', aliases=None):
    if aliases is None:
        aliases = []

    def decorator(func):
        func.command = name or func.__name__
        func.aliases = aliases

        return func

    return decorator(func) if func else decorator
