from django.urls import path
from . import views

urlpatterns = [
    path("login/discord/", views.discord_login, name="discord_login"),
    path("login/discord/callback/", views.discord_callback, name="discord_callback")
]
