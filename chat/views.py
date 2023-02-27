from django.shortcuts import render


def signin(request):
    return render(request, "chat/signin.html")


def signup(request):
    return render(request, "chat/signup.html")
