from datetime import datetime

from mongoengine import *


class URLLog(Document):

    url = URLField()
    first_nick = StringField()
    last_nick = StringField()

    counter = IntField(default=0)
    first_post = DateTimeField(default=datetime.now)
    last_post = DateTimeField()

    def save(self):
        if not self.first_nick:
            self.first_nick = self.last_nick

        super(URLLog, self).save()
