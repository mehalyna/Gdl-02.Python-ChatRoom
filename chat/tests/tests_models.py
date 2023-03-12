from django.core.management import call_command
from django.test import TestCase

from chat.models import Chat, User


class TestModels(TestCase):
    def setUp(self):
        # Load fixtures
        call_command("loaddata", "chat/fixtures/role_data.json", verbosity=0)
        call_command("loaddata", "chat/fixtures/user_data.json", verbosity=0)
        call_command("loaddata", "chat/fixtures/chat_data.json", verbosity=0)
        call_command("loaddata", "chat/fixtures/message_data.json", verbosity=0)

    def test_add_chat_member_new_member_returns_true(self):
        chat = Chat.objects.get(pk=1)
        size_before = chat.chat_member.all().count()
        user = User.objects.get(pk=9)
        chat.chat_member.add(user)
        size_after = chat.chat_member.all().count()
        self.assertEquals(size_before + 1, size_after)

    def test_add_chat_member_already_exits_returns_true(self):
        chat = Chat.objects.get(pk=1)
        size_before = chat.chat_member.all().count()
        user = User.objects.get(pk=5)
        chat.chat_member.add(user)
        size_after = chat.chat_member.all().count()
        self.assertEquals(size_before, size_after)
