import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render

from chat.models import Chat, Message


def handler404(request, exception):
    return render(request, "chat/404.html", status=404)


@login_required
def after_login(request):
    return


@login_required
def create_room(request):
    print(request)
    if request.method == "POST":
        chat_name = request.POST["room_name"]
        print(type(chat_name))
        # Create new room
        req_chat = Chat.objects.filter(chat_name=chat_name)

        if req_chat.exists():
            err = f"Error: {chat_name} Already exists!"
            return render(request, "chat/create_room.html", {"error": err})
        else:
            new_room = Chat.objects.create(chat_name=chat_name)
            print(new_room)
            # return HttpResponseRedirect('detail/'+str(new_room.id)+'/')
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
def view_chat(request, room_id):
    # chat = []
    # chat.append({"id": 1, "name": "Chat Harcodeado"})
    # return render(request, "chat/view_chat.html", {"chat": chat})
    # chat_room = Chat.objects.get(chat_name=room_name)
    chat_room, created = Chat.objects.get_or_create(id=room_id)
    # chat_room = get_object_or_404(Chat, chat_name=room_name)
    room_messages = Message.objects.filter(chat=chat_room)
    current_user = request.user
    # print("Messages!", room_messages)
    return render(
        request,
        "chat/view_chat.html",
        {
            "room": chat_room,
            "room_messages": room_messages,
            "current_user": current_user,
        },
    )


# @login_required
# def view_chat(request,id_chat):
#     chat=[]
#     chat.append({"id":id_chat,"name": "Chat Harcodeado"})
#     return render(request,'chat/view_chat.html',{"chat":chat})


@login_required
def allchats(request):
    # user = request.user
    # rooms = Chat.objects.filter(chat_member=user)
    user_chats = Chat.objects.filter(chat_member=request.user)

    # print(user_chats.chat_name)
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
    return redirect("viewchat", str(room_id))
