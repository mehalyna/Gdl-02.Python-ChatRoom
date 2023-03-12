from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.urls import re_path

from chat.consumers import ChatConsumer
from chat.models import Chat, Message, Role, User


class MyTests(TestCase):
    async def test_chat_consumer(self):
        # creates objects for db
        role = await database_sync_to_async(
            Role.objects.create, thread_sensitive=False
        )(role_name="user", description="pass")
        user = await database_sync_to_async(
            User.objects.create, thread_sensitive=False
        )(username="user", password="pass", email="user@example.com", role=role)
        chat = await database_sync_to_async(
            Chat.objects.create, thread_sensitive=False
        )(chat_name="chatExample", description="some text")

        application = URLRouter(
            [
                re_path(r"ws/chat/(?P<room_id>\w+)/$", ChatConsumer.as_asgi()),
            ]
        )
        communicator = WebsocketCommunicator(application, f"/ws/chat/{chat.id}/")
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        # checks connection
        assert connected

        await communicator.send_json_to({"message": "hello"})
        response = await communicator.receive_json_from()
        # checks msg send
        self.assertEqual("hello", response["message"])

        await communicator.send_json_to({"message": "@user"})
        response = await communicator.receive_json_from()
        # checks tagged_message type
        self.assertEqual("tagged_message", response["type"])

        await communicator.disconnect()
        msgCreated = await sync_to_async(
            Message.objects.filter(pk=1).exists, thread_sensitive=True
        )()
        # checks msg inserted in database
        assert msgCreated
