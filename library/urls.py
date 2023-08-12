from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_user, name="register"),
    path("login/", views.loginUser, name="login_user"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
]
