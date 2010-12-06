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
