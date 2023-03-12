from django.test import SimpleTestCase
from django.urls import resolve, reverse

from chat import views


class TestUrls(SimpleTestCase):
    def test_signup_url_returns_signup_view(self):
        url = reverse("signupuser")
        self.assertEquals(resolve(url).func, views.signup)

    def test_signin_url_returns_signin_view(self):
        url = reverse("loginuser")
        self.assertEquals(resolve(url).func, views.signin)

    def test_create_private_chat_url_returns_create_private_chat_view(self):
        url = reverse("create-private-chat")
        self.assertEquals(resolve(url).func, views.create_private_chat)

    def test_create_room_url_returns_create_room_view(self):
        url = reverse("create-room")
        self.assertEquals(resolve(url).func, views.create_room)

    def test_all_chats_url_returns_all_chats_view(self):
        url = reverse("allchats")
        self.assertEquals(resolve(url).func, views.allchats)

    def test_view_chat_url_returns_view_chat_view(self):
        url = reverse("viewchat", args=["1"])
        self.assertEquals(resolve(url).func, views.view_chat)

    def test_add_users_url_returns_add_users_view(self):
        url = reverse("add-users", args=["2"])
        self.assertEquals(resolve(url).func, views.add_users)

    def test_logout_url_returns_logout_user_view(self):
        url = reverse("logoutuser")
        self.assertEquals(resolve(url).func, views.logoutuser)

    def test_delete_message_url_returns_delete_msg_view(self):
        url = reverse("deletemsg", args=["17", "3"])
        self.assertEquals(resolve(url).func, views.deltemsg)

    def test_view_private_chat_url_returns_view_private_chat_view(self):
        url = reverse("view-private-chat", args=["4"])
        self.assertEquals(resolve(url).func, views.view_private_chat)
