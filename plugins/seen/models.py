import datetime

from mongoengine import *

class LastSeenModel(Document):

    nick = StringField()
    seen = DateTimeField(default = datetime.datetime.now)
    msg = StringField()

    def save(self):
        self.seen = datetime.datetime.now()
        super(LastSeenModel, self).save()

