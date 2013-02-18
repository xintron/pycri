import collections
import inspect
import sys


def _module_name(name):
    if name.startswith('pycri_'):
        return 'pycri.ext.'+name.split('_', 2)[1]
    if name.startswith('pycri'):
        return name


class IRCLibrary(type):
    def __init__(cls, name, bases, attrs):
        module_name = _module_name(cls.__module__.lower())
        class_name = name.lower()

        if not hasattr(cls, 'cache'):
            cls.cache = collections.defaultdict(dict)

        else:
            # Do not load classes that's already cached
            if not class_name in cls.cache[module_name]:
                cls.cache[module_name][class_name] = cls

        type.__init__(cls, name, bases, attrs)


class IRCObject(object):
    __metaclass__ = IRCLibrary

    commands = {}
    library = collections.defaultdict(dict)

    def _set_event(self, event):
        """Setter for command events."""
        self._event = event

    def _get_event(self):
        return self._event

    event = property(_get_event, _set_event)

    @classmethod
    def load(cls, module_name):
        module_name = _module_name(module_name)
        if not module_name:
            raise ImportError

        # Load module to register new IRCObject subclasses
        try:
            if sys.modules[module_name]:
                reload(sys.modules[module_name])
        except:
            __import__(module_name)

        plugins_to_instantiate = []

        # Load all plugins in the module
        for name, plugin in cls.cache[module_name].iteritems():
            plugins_to_instantiate.append((name, plugin))

        # Instantiate plugins and collect commands
        for name, plugin in plugins_to_instantiate:
            if not name in cls.library[module_name]:
                plugin_instance = plugin()

                for method_name, method in inspect.getmembers(plugin_instance):
                    if not method_name.startswith('_') \
                            and inspect.ismethod(method):
                        if hasattr(method, 'command'):
                            commands = [method.command] + method.aliases

                            for command in commands:
                                cls.commands[command] = method

                cls.library[module_name][name] = plugin_instance

    @classmethod
    def unload(cls, module_name):

        # Collect commands to unload
        commands_to_unload = []
        for command, method in cls.commands.iteritems():
            if method.im_self in cls.library[module_name].values():
                commands_to_unload.append(command)

        # Unload the commands
        for command in commands_to_unload:
            del cls.commands[command]

        del cls.cache[module_name]
        del cls.library[module_name]

    @classmethod
    def reload(cls, name):
        cls.unload(name)
        cls.load(name)
        return


def command(func=None, name='', aliases=None, inspect=True):
    if aliases is None:
        aliases = []
    inspect = bool(inspect)

    def decorator(func):
        func.command = name or func.__name__
        func.aliases = aliases
        func.inspect = inspect
        return func
    return decorator(func) if func else decorator
