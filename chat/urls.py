from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signupuser"),
    path("login/", views.signin, name="loginuser"),
]
