import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import Chat, Message, User


def handler404(request, exception):
    return render(request, "chat/404.html", status=404)


@login_required
def create_private_chat(request):
    if request.method == "POST":
        friend_username = request.POST["username"]
        user = User.objects.filter(username=friend_username).first()

        if not user:
            err = f"Error: User {friend_username} does not exist!"
            return render(request, "chat/create_private_chat.html", {"error": err})

        priv_chat_name = f"{request.user.username} - {friend_username}"
        name_of_chat = Chat.objects.filter(chat_name=priv_chat_name)
        priv_chat_name_2 = f"{friend_username} - {request.user.username}"
        name_of_chat_2 = Chat.objects.filter(chat_name=priv_chat_name_2)

        if name_of_chat.exists() or name_of_chat_2.exists():
            err = f"Error: Chat with {friend_username} already exists!"
            return render(request, "chat/create_private_chat.html", {"error": err})

        else:
            new_private_chat = Chat.objects.create(
                chat_name=priv_chat_name, description="Private"
            )
            new_private_chat.chat_member.add(request.user, user)
            return redirect("view-private-chat", str(new_private_chat.id))

    else:
        err = ""
        return render(request, "chat/create_private_chat.html", {"error": err})


def after_login(request):
    return


@login_required
def create_room(request):
    if request.method == "POST":
        chat_name = request.POST["room_name"]
        # Create new room
        req_chat = Chat.objects.filter(chat_name=chat_name)

        if req_chat.exists():
            err = f"Error: {chat_name} Already exists!"
            return render(request, "chat/create_room.html", {"error": err})
        else:
            new_room = Chat.objects.create(chat_name=chat_name)
            return redirect("viewchat", str(new_room.id))
    else:
        err = ""
        return render(request, "chat/create_room.html", {"error": err})


def signin(request):
    if request.user.is_authenticated:
        return redirect("allchats")
    else:
        if request.method == "GET":
            return render(request, "chat/signin.html")
        else:
            user = authenticate(
                request,
                username=request.POST["username"],
                password=request.POST["password"],
            )
            if user is None:
                return render(
                    request,
                    "chat/signin.html",
                    {"error": "Username or password did not match"},
                )
            else:
                login(request, user)
                return redirect("allchats")


# base_url="http://pychat.lat"
base_url = "http://127.0.0.1:8000"


def signup(request):
    if request.user.is_authenticated:
        return redirect("allchats")
    else:
        if request.method == "GET":
            return render(request, "chat/signup.html")
        else:
            try:
                myobjR = {
                    "username": request.POST["username"],
                    "email": request.POST["email"],
                    "password1": request.POST["password1"],
                    "password2": request.POST["password2"],
                }
                if request.POST["password1"] == request.POST["password2"]:
                    urlR = f"{base_url}/dj-rest-auth/registration/"
                    userR = requests.post(urlR, json=myobjR)
                    if userR:
                        user = authenticate(
                            request,
                            username=request.POST["username"],
                            password=request.POST["password2"],
                        )
                        login(request, user)
                        return redirect("allchats")
                    else:
                        err = "The username has already been taken. Please choose a new username"
                        return render(request, "chat/signup.html", {"error": err})
                else:
                    err = "The passwords not match"
                    return render(request, "chat/signup.html", {"error": err})

            except IntegrityError:
                err = (
                    "The username has already been taken. Please choose a new username"
                )
                return render(request, "chat/signup.html", {"error": err})


@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("loginuser")


@login_required
def view_chat(request, room_id):
    chat_room, created = Chat.objects.get_or_create(id=room_id)
    priv_room = Chat.objects.filter(id=room_id, description="Private").first()
    if priv_room:
        return render(request, "chat/404.html")
    room_messages = Message.objects.filter(chat=chat_room)
    current_user = request.user
    return render(
        request,
        "chat/view_chat.html",
        {
            "room": chat_room,
            "room_messages": room_messages,
            "current_user": current_user,
        },
    )


@login_required
def allchats(request):
    user_chats = Chat.objects.filter(chat_member=request.user)

    return render(
        request,
        "chat/allchats.html",
        {
            "rooms": user_chats,
        },
    )


def deltemsg(request, msg_id, room_id):
    msgDel = Message.objects.get(pk=msg_id)
    msgDel.delete()
    chat_desc = Chat.objects.get(pk=room_id).description

    if chat_desc == "Private":
        return redirect("view-private-chat", str(room_id))

    else:
        return redirect("viewchat", str(room_id))


@login_required
def view_private_chat(request, room_id):
    chat_room, created = Chat.objects.get_or_create(id=room_id)
    room_messages = Message.objects.filter(chat=chat_room)
    current_user = request.user
    chat = get_object_or_404(Chat, id=room_id)
    if current_user not in chat.chat_member.all():
        return render(request, "chat/404.html")
    return render(
        request,
        "chat/view_chat.html",
        {
            "room": chat_room,
            "room_messages": room_messages,
            "current_user": current_user,
        },
    )
