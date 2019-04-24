import responder
from responder import Request, Response
from database import PokebelUser, PokebelMessage, KeitaiUser, KeitaiMessage, create_tables
from globals import Generation

api = responder.API(cors=True)


@api.route('/pokebel/messages')
async def get_pokebel_messages(req: Request, resp: Response):
    json = await req.media()

    print(json)

    user = PokebelUser.get_or_none(PokebelUser.number == json['number'])
    print(user)

    if not user:
        resp.media = []

    query = (PokebelMessage
             .select()
             .where(PokebelMessage.from_user == user)
             .order_by(PokebelMessage.created_at))

    resp.media = [{
        "user": {
            "id": msg.to_user.id,
            "number": msg.to_user.number,
        },
        "content": msg.content,
        "created_at": msg.created_at.isoformat(),
    } for msg in query]


@api.route('/pokebel/send')
async def create_pokebel_messages(req: Request, resp: Response):
    json = await req.media()
    print(json)

    from_user, created = PokebelUser.get_or_create(number=json['from_number'])
    if created:
        from_user.save()
    to_user, created = PokebelUser.get_or_create(number=json['to_number'])
    if created:
        to_user.save()

    message = PokebelMessage.create(from_user=from_user, to_user=to_user, content=123456)
    message.save()


if __name__ == '__main__':
    create_tables()
    api.run()
