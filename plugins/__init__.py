import collections
import imp
import inspect


class PluginLibrary(type):
    def __init__(cls, name, bases, attrs):
        module_name = cls.__module__.lower()
        class_name = name.lower()

        if not hasattr(cls, 'cache'):
            cls.cache = collections.defaultdict(dict)

        else:
            # Do not load classes that's already cached
            if not class_name in cls.cache[module_name]:
                cls.cache[module_name][class_name] = cls

        type.__init__(cls, name, bases, attrs)


class Plugin(object):
    __metaclass__ = PluginLibrary

    commands = {}
    library = collections.defaultdict(dict)

    @classmethod
    def load(cls, name):
        module_name, plugin_name = name.split('.') if '.' in name else (name, '')

        # Load module to register new Plugin subclasses
        try:
            fp, pathname, description = imp.find_module(module_name, ['plugins'])
            imp.load_module(module_name, fp, pathname, description)

        finally:
            if fp:
                fp.close()

        plugins_to_instantiate = []

        if plugin_name:
            # Load specific plugin from module
            plugin = cls.cache[module_name][plugin_name]
            plugins_to_instantiate.append((plugin_name, plugin))

        else:
            # Load all plugins in the module
            for name, plugin in cls.cache[module_name].iteritems():
                plugins_to_instantiate.append((name, plugin))

        # Instantiate plugins and collect commands
        for name, plugin in plugins_to_instantiate:
            if not name in cls.library[module_name]:
                plugin_instance = plugin()

                for method_name, method in inspect.getmembers(plugin_instance):
                    if not method_name.startswith('_') and inspect.ismethod(method):
                        if hasattr(method, 'command'):
                            commands = [method.command] + method.aliases

                            for command in commands:
                                cls.commands[command] = method

                cls.library[module_name][name] = plugin_instance

    @classmethod
    def unload(cls, name):
        module_name, plugin_name = name.split('.') if '.' in name else (name, '')

        # Collect commands to unload
        commands_to_unload = []
        for command, method in cls.commands.iteritems():
            unload = False

            if plugin_name:
                if method.im_self is cls.library[module_name][plugin_name]:
                    unload = True
            else:
                if method.im_self in cls.library[module_name].values():
                    unload = True

            if unload:
                commands_to_unload.append(command)

        # Unload the commands
        for command in commands_to_unload:
            del cls.commands[command]

        # Unload single plugin or the entire module
        if plugin_name:
            del cls.cache[module_name][plugin_name]
            del cls.library[module_name][plugin_name]

        else:
            del cls.cache[module_name]
            del cls.library[module_name]

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
