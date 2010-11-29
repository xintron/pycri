import datetime, random
from mongoengine import *

from utils import base
from utils.timesince import timesince

class LastSeenModel(Document):

    nick = StringField()
    seen = DateTimeField(default = datetime.datetime.now)
    msg = StringField()

    def save(self):
        self.seen = datetime.datetime.now()
        super(LastSeenModel, self).save()

class LastSeen(base.Command):

    _plugin_name = 'last_seen'

    triggers = {
        'last_seen': ['seen'],
    }

    def last_seen(self, irc, user, channel, args):
        if len(args) > 0:
            try:
                u = LastSeenModel.objects.get(nick = args[0])
            except LastSeenModel.DoesNotExist:
                irc.msg(channel, 'I have not seen {}'.format(args[0]))
                return

        else:
            u = LastSeenModel.objects.all()
            u = u[random.randint(0, u.count()-1)]

        irc.msg(channel, '{} was last seen {} ago: {}'.format(u.nick, timesince(u.seen), u.msg))

    def on_privmsg(self, irc, user, channel, msg):
        user = user.split('!')[0]

        u, created = LastSeenModel.objects.get_or_create(nick = user)
        u.msg = msg
        u.save()
