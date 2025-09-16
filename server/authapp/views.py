from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
import requests

# Create your views here.

# this code is totally chatgpt'd btw im assuming the discord integration is gonna look more or less the same regardless
def discord_login(request):
    client_id = settings.DISCORD_CLIENT_ID
    scope = "identify email"
    return redirect(
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={client_id}&redirect_uri={redirect_uri}"
        f"&response_type=code&scope={scope}"
    )

def discord_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("/")

    # Exchange code for tokens
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.DISCORD_REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    tokens = r.json()
    access_token = tokens["access_token"]

    # Get user info
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get("https://discord.com/api/users/@me", headers=headers)
    r.raise_for_status()
    profile = r.json()

    discord_id = profile["id"]
    username = profile["username"]
    email = profile.get("email")

    # Tie to Django user
    user, _ = User.objects.get_or_create(
        username=f"discord_{discord_id}",
        defaults={"email": email or ""}
    )

    login(request, user)  # starts Django session
    return redirect("/")  # or send them to your fronten
