# HeiseiChatServer

## 始め方

```bash
$ brew install pipenv # なければインストール
$ cd /path/to/HeiseiChatServer
$ pipenv install
$ pipenv run python app.py
```

## 使い方

### ポケベルのメッセージを送る

```
POST /pokebel/messages/send

{
  "from_number": 8019136229,
  "to_number": 9089922241,
  "content": "12344566654"
}
```

### 受け取ったメッセージを一覧

```
POST /pokebel/messages

{
  "number": 00000000000
}
```

レスポンス

```
[
  {
    "user": {
      "id": 2,
      "number": 11111111111
    },
    "content": "123456",
    "created_at": "2019-04-24T18:21:19.790420"
  },
  {
    "user": {
      "id": 2,
      "number": 11111111111
    },
    "content": "123456",
    "created_at": "2019-04-24T18:21:19.964525"
  },
```