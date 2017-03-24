from peewee import *

db = SqliteDatabase('for_admin.db')

class Users(Model):
    username = CharField()
    password = CharField()
    created_at = DateField()
    is_admin = BooleanField()
    is_active = BooleanField()
    score = IntegerField()
    solved = CharField()

    class Meta:
        database = db

db.create_tables([Users],True)
