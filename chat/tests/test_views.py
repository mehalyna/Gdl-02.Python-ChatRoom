from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from chat.models import Chat, Message, User


class TestViews(TestCase):
    def setUp(self):
        # Load fixtures
        call_command("loaddata", "chat/fixtures/role_data.json", verbosity=0)
        self.client = Client()
        self.user = User.objects.create_user(
            username="usertest", password="pass", email="user@example.com"
        )
        self.user.save()

    def test_create_private_chat_view_POST_returns_302(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("create-private-chat"), {"username": self.user.username}
        )
        self.assertEquals(response.status_code, 302)

    def test_create_room_view_POST_returns_302(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("create-room"), {"room_name": "roomtest"})
        self.assertEquals(response.status_code, 302)

    def test_signup_view_POST_returns_302(self):
        client = Client()
        response = client.post(
            reverse("signupuser"),
            {
                "username": "foo",
                "password1": "bar",
                "password2": "bar",
                "email": "user@example.com",
            },
        )
        self.assertEquals(response.status_code, 302)

    def test_signin_view_POST_returns_200(self):
        client = Client()
        response = client.post(
            reverse("loginuser"), {"username": "foo", "password": "bar"}
        )
        self.assertEquals(response.status_code, 200)

    def test_logout_view_POST_returns_302(self):
        client = Client()
        client.login(username="foo", password="bar")
        response = self.client.post(reverse("logoutuser"))
        self.assertEquals(response.status_code, 302)

    def test_view_chat_view_returns_200(self):
        chat_room = Chat.objects.create(
            chat_name="chatExample", description="some text"
        )
        room_messages = Message.objects.filter(chat=chat_room)
        current_user = User.objects.create(
            username="user1",
            password="password",
            email="user1@example.com",
        )
        client = Client()
        client.force_login(current_user)
        response = client.post(
            reverse("viewchat", args=[chat_room.id]),
            {
                "room": chat_room,
                "room_messages": room_messages,
                "current_user": current_user,
            },
        )
        self.assertEquals(response.status_code, 200)

    def test_view_private_chat_view_returns_200(self):
        chat_room = Chat.objects.create(
            chat_name="chatExample", description="some text"
        )
        room_messages = Message.objects.filter(chat=chat_room)
        current_user = User.objects.create(
            username="user1",
            password="password",
            email="user1@example.com",
        )
        client = Client()
        client.force_login(current_user)
        response = client.post(
            reverse("view-private-chat", args=[chat_room.id]),
            {
                "room": chat_room,
                "room_messages": room_messages,
                "current_user": current_user,
            },
        )
        self.assertEquals(response.status_code, 200)

    def test_add_users_view_POST_returns_302(self):
        chat_room = Chat.objects.create(
            chat_name="chatExample2", description="some text"
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("add-users", args=[chat_room.id]), {"username": self.user.username}
        )
        self.assertEquals(response.status_code, 302)

    def test_all_chats_GET_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("allchats"))
        self.assertEquals(response.status_code, 200)
