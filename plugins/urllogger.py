import datetime, re
from mongoengine import *

from utils import base

class URLLogModel(Document):

    url = URLField()
    first_nick = StringField()
    last_nick = StringField()
    
    counter = IntField(default = 0)
    first_post = DateTimeField(default = datetime.datetime.now)
    last_post = DateTimeField()

    def save(self):
        if not self.first_nick:
            self.first_nick = self.last_nick

        super(URLLogModel, self).save()


class URLLog(base.Plugin):

    _plugin_name = 'URLLogger'

    def on_privmsg(self, irc, user, channel, msg):
        user = user.split('!')[0]

        m = re.findall('(https?://[^\s$]+)+', msg)
        if m:
            for url in m:
                u, created = URLLogModel.objects.get_or_create(url = url)

                if not u.first_nick:
                    u.first_nick = user

                u.last_nick = user
                u.last_post = datetime.datetime.now()

                if u.counter > 0:
                    irc.msg(channel, '.OLD {}. This url has been posted before on {} by {} (Times posted: {})'.format(
                        user,
                        '{} {} {} at {}:{}'.format(u.first_post.day, u.first_post.strftime('%b'), u.first_post.year, u.first_post.hour, u.first_post.minute),
                        u.first_nick,
                        u.counter
                    ))

                u.counter += 1

                u.save()
