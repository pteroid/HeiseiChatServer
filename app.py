import responder
from responder import Request, Response
from database import User, PokebelMessage, KeitaiMessage, create_tables
from globals import MojiType

api = responder.API(cors=True)


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
        "from_user": {
            "id": msg.from_user.id,
            "number": msg.from_user.number,
        },
        "content": msg.content,
        "created_at": msg.created_at.isoformat(),
    } for msg in query]


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
        "to_user": {
            "id": msg.to_user.id,
            "number": msg.to_user.number,
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

    message = PokebelMessage.create(from_user=from_user, to_user=to_user,
                                    content=json['content'])
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
        "from_user": {
            "id": msg.from_user.id,
            "email": msg.from_user.email,
        },
        "title": msg.title,
        "content": msg.content,
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
        "to_user": {
            "id": msg.to_user.id,
            "email": msg.to_user.email,
        },
        "title": msg.title,
        "content": msg.content,
        "created_at": msg.created_at.isoformat(),
    } for msg in query]


@api.route('/keitai/messages/send')
async def create_keitai_messages(req: Request, resp: Response):
    json = await req.media()

    from_user, created = User.get_or_create(email=json['from_email'])
    if created:
        from_user.save()
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
