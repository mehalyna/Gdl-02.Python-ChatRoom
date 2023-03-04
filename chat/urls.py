from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signupuser"),
    path("login/", views.signin, name="loginuser"),
    path("create-room/", views.create_room, name="create-room"),
    path("allchats/", views.allchats, name="allchats"),
    path("view-chat/", views.view_chat, name="viewchat"),
    # path("view-chat/<int:id_chat>", views.view_chat, name="viewchat"),
    path("logout/", views.logoutuser, name="logoutuser"),
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="chat-room"),
    # path("<str:room_name>/", views.previous_messages, name="previous_messages"),
]
