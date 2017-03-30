from peewee import *

db_for_admin = SqliteDatabase('for_admin.db')
db = SqliteDatabase('m1z0r3ctf.db')

class Users(Model):
    username = CharField()
    password = CharField()
    created_at = DateField()
    is_admin = BooleanField()
    is_active = BooleanField()
    score = IntegerField()
    solved = CharField()

    class Meta:
        database = db_for_admin

db_for_admin.create_tables([Users],True)

class Problems(Model):
    name = CharField()
    point = IntegerField()
    genre = CharField()
    flag = CharField()
    detail = CharField()
    author = CharField()

    class Meta:
        database = db

db.create_tables([Problems],True)
