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


class PokebelUser(BaseModel):
    number = IntegerField(unique=True)


class PokebelMessage(BaseModel):
    from_user = ForeignKeyField(PokebelUser, backref='from_user')
    to_user = ForeignKeyField(PokebelUser, backref='to_user')
    created_at = DateTimeField(default=datetime.datetime.now)
    content = TextField()


class KeitaiUser(BaseModel):
    email = CharField(unique=True)


class KeitaiMessage(BaseModel):
    from_user = ForeignKeyField(KeitaiUser, backref='from_user')
    to_user = ForeignKeyField(KeitaiUser, backref='to_user')
    created_at = DateTimeField(default=datetime.datetime.now)
    generation = GenerationField()
    title = TextField(null=True)
    content = TextField()


def create_tables():
    with database:
        database.create_tables([PokebelUser, PokebelMessage, KeitaiUser, KeitaiMessage])
