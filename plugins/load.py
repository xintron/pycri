from plugins import Plugin, command


class LoadPlugin(Plugin):
    @command
    def load(self, name):
        Plugin.load(name)

    @command
    def unload(self, name):
        Plugin.unload(name)

    @command
    def reload(self, name):
        if name == 'all':
            for module in Plugin.library:
                Plugin.reload(module)
        else:
            Plugin.reload(name)
