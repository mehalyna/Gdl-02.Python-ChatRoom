import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render

from chat.models import Chat, Message


def handler404(request, exception):
    return render(request, "chat/404.html", status=404)


@login_required
def create_room(request):
    return render(request, "chat/create_room.html")


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
            print(user)
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
                        print(userR.status_code)
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
def view_chat(request):
    chat = []
    chat.append({"id": 1, "name": "Chat Harcodeado"})
    return render(request, "chat/view_chat.html", {"chat": chat})


# @login_required
# def view_chat(request,id_chat):
#     chat=[]
#     chat.append({"id":id_chat,"name": "Chat Harcodeado"})
#     return render(request,'chat/view_chat.html',{"chat":chat})


@login_required
def allchats(request):
    return render(request, "chat/allchats.html")


def index(request):
    return render(
        request,
        "chat/index.html",
        {
            "rooms": Chat.objects.all(),
        },
    )


def previous_messages(request, room_name):
    room = Chat.objects.get(chat_name=room_name)
    return render(
        request,
        "chat/room.html",
        {"messages": Message.objects.filter(chat=room).order_by("-created_at")[:10]},
    )


def room(request, room_name):
    chat_room, created = Chat.objects.get_or_create(chat_name=room_name)
    return render(
        request,
        "chat/room.html",
        {
            "room": chat_room,
        },
    )


"""def room(request, message):
    chat_room, created = Chat.objects.delete(pk=message.)
    return render(
        request,
        "chat/room.html",
        {
            "room": chat_room,
        },
    )"""
