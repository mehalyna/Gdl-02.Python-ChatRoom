import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render


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
    id = [1, 2, 1, 1, 2, 1, 2, 1]
    message = ["Tenetur!", "hello", "there", "demo", "hi", "this", "is", "a"]
    hour = [
        "01:30 PM",
        "01:31 PM",
        "01:32 PM",
        "01:33 PM",
        "01:34 PM",
        "01:35 PM",
        "01:36 PM",
        "01:37 PM",
    ]
    date = [
        "Aug 13",
        "Aug 13",
        "Aug 13",
        "Aug 13",
        "Aug 13",
        "Aug 13",
        "Aug 13",
        "Aug 13",
    ]
    chat = zip(id, message, hour, date)
    return render(request, "chat/view_chat.html", {"chat": chat})


# @login_required
# def view_chat(request,id_chat):
#     chat=[]
#     chat.append({"id":id_chat,"name": "Chat Harcodeado"})
#     return render(request,'chat/view_chat.html',{"chat":chat})


@login_required
def allchats(request):
    return render(request, "chat/allchats.html")
