import datetime, re, random

from mongoengine import connect

from models import URLLog
from plugins import Plugin, command
import settings
from utils import timesince


if settings.DB_NAME:
    connect(settings.DB_NAME)


class URLLogger(Plugin):
    def on_privmsg(self, irc, prefix, params):
        user = prefix.split('!')[0]
        channel = params[0]
        msg = params[-1]

        m = re.findall('(https?://[^\s$]+)+', msg)
        if m:
            for url in m:
                u, created = URLLog.objects.get_or_create(url = url)

                if not u.first_nick:
                    u.first_nick = user

                u.last_nick = user
                u.last_post = datetime.datetime.now()

                if u.counter > 0:
                    irc.msg(channel, 'OLD! This url was first posted {} ago by {} (Times posted: {})'.format(timesince(u.first_post), u.first_nick, u.counter))

                u.counter += 1

                u.save()

    @command(aliases=['rurl'])
    def random_url(self):
        u = URLLog.objects.all()
        u = u[random.randint(0, u.count() - 1)]

        msg = '{url} first posted {time} ago by {nick} (Times posted: {count})'.format(
            url=u.url,
            time=timesince(u.first_post),
            nick=u.first_nick,
            count=u.counter
        )

        irc.msg(channel, msg)
