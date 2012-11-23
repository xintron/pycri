import random

from pycri.plugins import IRCObject, command


class Dice(IRCObject):
    @command
    def roll(self, dice):
        '''Rolls a dice according to roleplaying notation. Example: !roll 2d6, rolls two 6-sided dices.'''
        multiplier, sides = (int(x) for x in dice.split('d'))
        result = random.choice(xrange(multiplier, multiplier * sides + 1))

        return result
