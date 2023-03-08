from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signupuser"),
    path("login/", views.signin, name="loginuser"),
    path("create-room/", views.create_room, name="create-room"),
    path("create-private-chat/", views.create_private_chat, name="create-private-chat"),
    path("allchats/", views.allchats, name="allchats"),
    path("detail/<int:room_id>/", views.view_chat, name="viewchat"),
    path("logout/", views.logoutuser, name="logoutuser"),
    path("detail/<int:msg_id>/<int:room_id>/delete", views.deltemsg, name="deletemsg"),
    path(
        "private-chat/<int:room_id>/", views.view_private_chat, name="view-private-chat"
    ),
]
