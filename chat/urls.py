from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signupuser"),
    path("login/", views.signin, name="loginuser"),
    path("create-room/", views.create_room, name="create-room"),
    path("allchats/", views.allchats, name="allchats"),
    path("detail/<int:room_id>/", views.view_chat, name="viewchat"),
    # path("view-chat/<int:id_chat>", views.view_chat, name="viewchat"),
    path("logout/", views.logoutuser, name="logoutuser"),
    path("detail/<int:msg_id>/<int:room_id>/delete", views.deltemsg, name="deletemsg"),
]
