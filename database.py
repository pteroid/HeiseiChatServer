from peewee import *
from playhouse.shortcuts import model_to_dict
from enum import Enum, auto
import datetime
from globals import Generation

database = SqliteDatabase('test.db')


class BaseModel(Model):
    class Meta:
        database = database


class GenerationField(Field):
    field_type = 'INT'

    def db_value(self, value: Generation):
        return value.value

    def python_value(self, value):
        return Generation(value)


class User(BaseModel):
    number = IntegerField(unique=True, null=True)
    email = CharField(unique=True, null=True)


class PokebelMessage(BaseModel):
    from_user = ForeignKeyField(User, backref='from_user')
    to_user = ForeignKeyField(User, backref='to_user')
    created_at = DateTimeField(default=datetime.datetime.now)
    content = TextField()


class KeitaiMessage(BaseModel):
    from_user = ForeignKeyField(User, backref='from_user')
    to_user = ForeignKeyField(User, backref='to_user')
    created_at = DateTimeField(default=datetime.datetime.now)
    generation = GenerationField()
    title = TextField(null=True)
    content = TextField()


def create_tables():
    with database:
        database.create_tables([User, PokebelMessage, KeitaiMessage])
