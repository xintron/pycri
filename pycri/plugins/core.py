from pycri.plugins import Plugin, command


class Help(Plugin):
    @command
    def help(self, command):
        '''Displays a brief explanation of a given command. Example: !help help'''
        try:
            command_documentation = self.commands[command].__doc__
        except KeyError:
            return 'No such command.'

        if not command_documentation:
            command_documentation = 'No documentation found for !{}.'.format(command)

        return command_documentation


class Load(Plugin):
    @command
    def load(self, name, *plugins):
        '''Loads the specified plugin. Example: !load dice'''
        try:
            Plugin.load(name, *plugins)
        except ImportError:
            return 'Could not load {0}'.format(name)
        return '{0} was successfully loaded'.format(name)
    @command
    def unload(self, name, *plugins):
        '''Unloads the specified plugin. Example: !unload dice'''
        try:
            Plugin.unload(name, *plugins)
            return '{0} was successfully unloaded'.format(name)
        except KeyError:
            return 'No such plugin is currently loaded. Try !load {0}'.format(name)

    @command
    def reload(self, name='all'):
        '''Reloads the specified plugin. Example: !reload dice'''
        try:
            if name == 'all':
                keys = [x for x in Plugin.library.iterkeys()]
                for module in keys:
                    Plugin.reload(module)
                return 'All plugins were successfully reloaded.'
            else:
                Plugin.reload(name)
                return '{0} were successfully reloaded.'.format(name)
        except KeyError:
            return 'No such plugin is currently loaded. Try !load {0}'.format(name)
