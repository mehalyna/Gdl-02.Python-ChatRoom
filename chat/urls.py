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
]
