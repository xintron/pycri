import random

from plugins import Plugin, command


class Dice(Plugin):
    @command
    def roll(self, dice):
        '''
        Rolls a dice according to roleplaying notation::

            2d6 = Sum of two six-sided dices
            1d10 = A single ten-sided dice

        Example::

            !roll 2d6
            !roll 2d100
        '''

        multiplier, sides = (int(x) for x in dice.split('d'))
        result = random.choice(range(multiplier, multiplier * sides + 1))

        return result
