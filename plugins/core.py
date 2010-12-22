from plugins import Plugin, command


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
    def load(self, name):
        '''Loads the specified plugin. Example: !load dice'''
        try:
            Plugin.load(name)
        except ImportError:
            return 'No such plugin.'

    @command
    def unload(self, name):
        '''Unloads the specified plugin. Example: !unload dice'''
        Plugin.unload(name)

    @command
    def reload(self, name='all'):
        '''Reloads the specified plugin. Example: !reload dice'''
        try:
            if name == 'all':
                for module in Plugin.library:
                    Plugin.reload(module)
            else:
                Plugin.reload(name)
        except KeyError:
            return 'No such plugin is currently loaded. Try !load {0}'.format(name)
