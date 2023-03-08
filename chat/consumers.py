import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None

    def connect(self):
        self.room_id = int(self.scope["url_route"]["kwargs"]["room_id"])
        self.room_group_name = f"chat_{self.room_id}"
        self.user = self.scope["user"]
        self.room = Chat.objects.get(id=self.room_id)
        self.user_inbox = f"inbox_{self.user.username}"

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            # send the join event to the room
            self.room.online.add(self.user)
            self.room.chat_member.add(self.user)

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            self.room.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if not self.user.is_authenticated:
            return
        newMsg = Message.objects.create(user=self.user, chat=self.room, content=message)
        if message.startswith("@"):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "tagged_message",
                    "user": self.user.username,
                    "message": message,
                    "id": newMsg.id,
                },
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "user": self.user.username,
                    "message": message,
                    "id": newMsg.id,
                },
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def tagged_message(self, event):
        self.send(text_data=json.dumps(event))
