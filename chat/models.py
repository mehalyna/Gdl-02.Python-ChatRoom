from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=255)
    description = models.TextField()


class Permission(models.Model):
    permission_name = models.CharField(max_length=255)
    role = models.ManyToManyField("Role", related_name="permissions")


class User(AbstractUser):
    role = models.ForeignKey("Role", on_delete=models.CASCADE, default=1)


class Chat(models.Model):
    chat_name = models.CharField(max_length=255)
    max_size = models.IntegerField(default=30)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active_status = models.BooleanField(default=True)
    chat_member = models.ManyToManyField("User", related_name="chats")
    moderator = models.ManyToManyField("User", related_name="chats_mod")

    def get_online_count(self):
        return self.chat_member.count()

    def join(self, user):
        self.chat_member.add(user)
        self.save()

    def leave(self, user):
        self.chat_member.remove(user)
        self.save()

    def __str__(self):
        return f"{self.chat_name} ({self.get_online_count()})"


class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.content} [{self.created_at}]"

    def delete_message(message):
        Message.objects.get(pk=message.id).delete()

    def last_messages(roomName):
        room = Chat.objects.get(chat_name=roomName)
        return Message.objects.filter(chat=room).order_by("-created_at")[:10]
