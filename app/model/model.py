from peewee import *

db = SqliteDatabase('m1z0r3ctf.db')

class Users(Model):
    username = CharField()
    password = CharField()
    created_at = DateField()
    is_active = BooleanField()
    score = IntegerField()
    solved = CharField()

    class Meta:
        database = db

class Problems(Model):
    name = CharField()
    point = IntegerField()
    genre = CharField()
    flag = CharField()
    detail = CharField()
    author = CharField()

    class Meta:
        database = db

db.create_tables([Users, Problems],True)
