import responder
from responder import Request, Response
from database import User, PokebelMessage, KeitaiMessage, create_tables
from globals import MojiType
from heisei_chat_ml.heisei_chat_ml import text_to_pkebell as pokebell

api = responder.API(cors=True, cors_params={
    'allow_origins': ['*'],
    'allow_methods': ['*'],
    'allow_headers': ['*'],
})


@api.route('/login')
async def create_new_user_account(req: Request, resp: Response):
    json = await req.media()
    print(json)

    if not (json['number'] and json['email'] and json['username']):
        return

    user = User.get_or_none((User.number == json['number']) | (User.email == json['email']))

    if not user:
        user = User.create()
        message = KeitaiMessage.create(from_user=User.get(User.email == "information@i.softban.jp"), to_user=user,
                                       moji_type=MojiType.EMOJI,
                                       title="【お客さま限定】10,000円割引クーポンプレゼント",
                                       content="""ガラケーをご利用中のお客さま限定で、機種変更に使えるクーポンをプレゼント🎁

        【特別クーポン】
        機種代金が税込10,000円割引！

        有効期限：5月31日(金)まで

        対象機種など詳細はこちらをご確認ください。
        http://u.softbank.jp/CsR7dVt
        （アクセスには通信料がかかります）

        さらに【スマホスタート割】でガラケーから対象のスマホにすると機種代金が税込10,800円割引になります。※

        令和を新しいスマホで迎えよう!
        ゴールデンウィークはソフトバンク取扱店へぜひお越しください


        ※ 通話基本プランの2年契約／2年契約（フリープラン）またはハートフレンド割引に加入すること。学割放題との併用はできません。""")
        message.save()
        print("sample messages created")

    user.number = json['number']
    user.email = json['email']
    user.username = json['username']

    user.save()

    print(user)
    resp.status_code = api.status_codes.HTTP_200


@api.route('/pokebel/messages/received')
async def get_received_pokebel_messages(req: Request, resp: Response):
    json = await req.media()

    print(json)

    to_user = User.get_or_none(User.number == json['number'])

    if not to_user:
        resp.media = []

    query = (PokebelMessage
             .select()
             .where(PokebelMessage.to_user == to_user)
             .order_by(PokebelMessage.created_at))

    resp.media = [{
        "id": msg.id,
        "from_user": {
            "id": msg.from_user.id,
            "number": msg.from_user.number,
            "username": msg.from_user.username,
        },
        "content": msg.content,
        "created_at": msg.created_at.isoformat(),
    } for msg in query]


@api.route('/pokebel/convert')
async def convert_text_to_pokebell_style(req: Request, resp: Response):
    json = await req.media()

    words, numbers = pokebell.text_to_pkebell(json["text"], threshold=0.5)

    resp.media = {
        "words": words,
        "numbers": numbers,
    }


@api.route('/pokebel/messages/sent')
async def get_sent_pokebel_messages(req: Request, resp: Response):
    json = await req.media()

    from_user = User.get_or_none(User.number == json['number'])

    if not from_user:
        resp.media = []

    query = (PokebelMessage
             .select()
             .where(PokebelMessage.from_user == from_user)
             .order_by(PokebelMessage.created_at))

    resp.media = [{
        "id": msg.id,
        "to_user": {
            "id": msg.to_user.id,
            "number": msg.to_user.number,
            "username": msg.from_user.username,
        },
        "content": msg.content,
        "created_at": msg.created_at.isoformat(),
    } for msg in query]


@api.route('/pokebel/messages/send')
async def create_pokebel_messages(req: Request, resp: Response):
    json = await req.media()
    print(json)

    from_user, created = User.get_or_create(number=json['from_number'])
    if created:
        from_user.save()
    to_user, created = User.get_or_create(number=json['to_number'])
    if created:
        to_user.save()

    words, numbers = pokebell.text_to_pkebell(json["content"], threshold=0.5)

    number_content = ""
    for n in numbers:
        number_content += n

    message = PokebelMessage.create(from_user=from_user, to_user=to_user,
                                    content=number_content)
    message.save()


@api.route('/keitai/messages/received')
async def get_received_keitai_messages(req: Request, resp: Response):
    json = await req.media()

    to_user = User.get_or_none(User.email == json['email'])

    if not to_user:
        resp.media = []

    query = (KeitaiMessage
             .select()
             .where(KeitaiMessage.to_user == to_user)
             .order_by(KeitaiMessage.created_at))

    resp.media = [{
        "id": msg.id,
        "from_user": {
            "id": msg.from_user.id,
            "email": msg.from_user.email,
            "username": msg.from_user.username,
        },
        "title": msg.title,
        "content": msg.content,
        "content_dict": pokebell.text_to_dic(msg.content),
        "created_at": msg.created_at.isoformat(),
    } for msg in query]


@api.route('/keitai/messages/sent')
async def get_sent_keitai_messages(req: Request, resp: Response):
    json = await req.media()

    from_user = User.get_or_none(User.email == json['email'])

    if not from_user:
        resp.media = []

    query = (KeitaiMessage
             .select()
             .where(KeitaiMessage.from_user == from_user)
             .order_by(KeitaiMessage.created_at))

    resp.media = [{
        "id": msg.id,
        "to_user": {
            "id": msg.to_user.id,
            "email": msg.to_user.email,
            "username": msg.from_user.username,
        },
        "title": msg.title,
        "content": msg.content,
        "content_dict": pokebell.text_to_dic(msg.content),
        "created_at": msg.created_at.isoformat(),
    } for msg in query]


@api.route('/keitai/messages/send')
async def create_keitai_messages(req: Request, resp: Response):
    json = await req.media()

    print(json)

    from_user, created = User.get_or_create(email=json['from_email'])
    if created:
        print("from user created")
        from_user.save()
        print("to user created")
    to_user, created = User.get_or_create(email=json['to_email'])
    if created:
        to_user.save()

    print(from_user.id)

    message = KeitaiMessage.create(from_user=from_user, to_user=to_user,
                                   moji_type=MojiType[json['moji_type'].upper()],
                                   title=json['title'],
                                   content=json['content'])
    message.save()


if __name__ == '__main__':
    create_tables()
    api.run()
