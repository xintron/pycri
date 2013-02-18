from pycri.plugins import IRCObject, command
from pycri.globals import g
from pycri.signals import extension_setup, extension_teardown

logger = g.getLogger('core-plugin')


class Help(IRCObject):
    @command
    def help(self, command):
        """Displays a brief explanation of a given command. Example: !help help
        """
        try:
            command_documentation = self.commands[command].__doc__
        except KeyError:
            return 'No such command.'

        if not command_documentation:
            command_documentation = 'No documentation found for !{}.'\
                .format(command)

        return command_documentation


class Load(IRCObject):

    @command
    def load(self, name, *plugins):
        '''Loads the specified plugin. Example: !load dice'''
        try:
            logger.debug('Loading {}'.format(name))
            IRCObject.load(name, *plugins)
        except ImportError:
            return 'Could not load {0}'.format(name)
        extension_setup.send(name)
        return '{0} was successfully loaded'.format(name)

    @command
    def unload(self, name, *plugins):
        '''Unloads the specified plugin. Example: !unload dice'''
        try:
            logger.debug('Unloading {}'.format(name))
            extension_teardown.send(name)
            IRCObject.unload(name, *plugins)
            return '{0} was successfully unloaded'.format(name)
        except KeyError:
            return 'No such plugin is currently loaded. Try !load {0}'\
                .format(name)

    @command
    def reload(self, name='all'):
        '''Reloads the specified plugin. Example: !reload dice'''
        try:
            if name == 'all':
                keys = [x for x in IRCObject.library.iterkeys()]
                logger.debug('Reloading all plugins')
                for module in keys:
                    IRCObject.reload(module)
                return 'All plugins were successfully reloaded.'
            else:
                logger.debug('Reloading {}'.format(name))
                IRCObject.reload(name)
                return '{0} were successfully reloaded.'.format(name)
        except KeyError:
            return 'No such plugin is currently loaded. Try !load {0}'\
                .format(name)

    @command
    def plugins(self, *args):
        """Method for listing loaded plugins."""
        loaded = []
        for key in IRCObject.library.iterkeys():
            loaded.append(key)
        return ','.join(loaded)
