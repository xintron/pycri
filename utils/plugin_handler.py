import sys, re
from copy import copy

prev = copy(sys.modules.values())
from plugins import *
main_plugin = None
new_plugins = []

for plugin in sys.modules.values():
    if not plugin:
        continue

    if plugin not in prev:
        if plugin.__name__ == 'plugins':
            main_plugin = plugin

        else:
            new_plugins.append(plugin)

new_plugins = filter(lambda x: re.match('^plugins\.', x.__name__), new_plugins)
