import datetime

from flask_peewee.auth import BaseUser
from peewee import *

from app import db

class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username

class Album(db.Model):
    user = ForeignKeyField(User)
    title = CharField()
    has_elevation = BooleanField(default=False)
    basemap = CharField()
    track = CharField()
    
    def __unicode__(self):
        return self.title
    
class Photo(db.Model):
    user = ForeignKeyField(User)
    album = ForeignKeyField(Album)
    lat = FloatField()
    lng = FloatField()
    url = CharField()
    caption = CharField()
    thumbnail = CharField()
    
    def __unicode__(self):
        return self.caption
