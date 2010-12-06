from plugins import Plugin, command


class LoadPlugin(Plugin):
    @command
    def load(self, name):
        '''Loads the specified plugin. Example: !load dice'''
        Plugin.load(name)

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
