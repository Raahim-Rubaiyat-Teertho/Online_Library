from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_user, name="register"),
    path("login/", views.loginUser, name="login_user"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("upload_book/", views.upload_book, name = "upload_book"),
    path("search_book/", views.search_book, name="search_book"),
    path("confirm_rent/<str:pk>/", views.confirm_rent, name="confirm_rent"),
    path("payment_gateway/", views.payment, name="payment_gateway")
]
