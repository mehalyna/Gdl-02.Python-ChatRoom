from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=255)
    description = models.TextField()


class Permission(models.Model):
    permission_name = models.CharField(max_length=255)
    role = models.ManyToManyField("Role", related_name="permissions")


class User(AbstractUser):
    role = models.ForeignKey("Role", on_delete=models.CASCADE)


class Chat(models.Model):
    chat_name = models.CharField(max_length=255)
    max_size = models.IntegerField(default=30)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active_status = models.BooleanField(default=True)
    chat_member = models.ManyToManyField("User", related_name="chats")
    moderator = models.ManyToManyField("User", related_name="chats_mod")


class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey("Chat", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
