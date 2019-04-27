from peewee import *
from playhouse.shortcuts import model_to_dict
from enum import Enum, auto
import datetime
from globals import MojiType

database = SqliteDatabase('test.db')


class BaseModel(Model):
    class Meta:
        database = database


class MojiTypeField(Field):
    field_type = 'INT'

    def db_value(self, value: MojiType):
        return value.value

    def python_value(self, value):
        return MojiType(value)


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
    moji_type = MojiTypeField()
    title = TextField(null=True)
    content = TextField()


def create_tables():
    if User.table_exists():
        return

    with database:
        database.create_tables([User, PokebelMessage, KeitaiMessage])

    from_user = User.create(email="hoge@ezweb.ne.jp")
    from_user.save()
    to_user = User.create(email="fuga@docomo.ne.jp")
    to_user.save()

    message = KeitaiMessage.create(from_user=from_user, to_user=to_user,
                                   moji_type=MojiType.EMOJI,
                                   title="タイトル",
                                   content="本文")
    message.save()

    from_user = User.create(email="information@i.softban.jp")
    from_user.save()

    message = KeitaiMessage.create(from_user=from_user, to_user=to_user,
                                   moji_type=MojiType.EMOJI,
                                   title="【お客さま限定】10,000円割引クーポンプレゼント",
                                   content="""
ガラケーをご利用中のお客さま限定で、機種変更に使えるクーポンをプレゼント🎁

【特別クーポン】
機種代金が税込10,000円割引！

有効期限：5月31日(金)まで

対象機種など詳細はこちらをご確認ください。
http://u.softbank.jp/CsR7dVt
（アクセスには通信料がかかります）

さらに【スマホスタート割】でガラケーから対象のスマホにすると機種代金が税込10,800円割引になります。※

令和を新しいスマホで迎えよう!
ゴールデンウィークはソフトバンク取扱店へぜひお越しください


※ 通話基本プランの2年契約／2年契約（フリープラン）またはハートフレンド割引に加入すること。学割放題との併用はできません。
""")
    message.save()
    print("sample messages created")
