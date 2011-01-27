from mongoengine import connect

from plugins import Plugin, command
from utils.timeconversion import timesince
from utils.encoding import smart_unicode, smart_str
from plugins.seen.models import LastSeenModel

import settings


if settings.DB_NAME:
    connect(settings.DB_NAME)

class LastSeen(Plugin):

    @command
    def seen(self, nick):
        '''Outputs last statement by given nick.'''
        if nick == settings.NICKNAME:
            return 'I\'m right here dickhead!'

        try:
            u = LastSeenModel.objects.get(nick = nick)
        except LastSeenModel.DoesNotExist:
            return 'I have not seen {}.'.format(nick)

        return '{} was last seen {} ago: {}'.format(u.nick, timesince(u.seen), smart_str(u.msg))

    def on_privmsg(self, irc, prefix, params):
        user = prefix.split('!')[0]
        msg = params[-1]

        u, created = LastSeenModel.objects.get_or_create(nick = user)
        u.msg = smart_unicode(msg)
        u.save()
        return
