import imp

import settings


class PluginLibrary(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'library'):
            cls.library = {}
        else:
            cls.library[cls.__module__] = cls()

        type.__init__(cls, name, bases, attrs)

    def __repr__(cls):
        cls.__name__


class Plugin(object):
    __metaclass__ = PluginLibrary

    commands = {}

    def __repr__(self):
        return '{0}()'.format(self.__class__)

    @classmethod
    def autoload(cls):
        for plugin in settings.PLUGINS:
            cls.load(plugin)

    @classmethod
    def load(cls, name):
        fp, pathname, description = imp.find_module(name, ['plugins'])

        try:
            imp.load_module(name, fp, pathname, description)
        finally:
            if fp:
                fp.close()

    @classmethod
    def reload(cls, name):
        del cls.library[name]
        cls.load(name)

def command(func=None, name='', aliases=None):
    if aliases is None:
        aliases = []

    def decorator(func):
        module_method = '%s.%s' % (func.__module__, func.__name__)

        for alias in aliases:
            Plugin.commands[alias] = module_method

        Plugin.commands[name or func.__name__] = module_method

        return func

    return decorator(func) if func else decorator
