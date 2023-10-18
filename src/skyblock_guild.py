import requests
from dotenv import dotenv_values

api_hypixel = "https://api.hypixel.net/"
token_hypixel = dotenv_values()['HYPIXEL_KEY']


def return_discord_hypixel(uuid):
    req = requests.get(f"{api_hypixel}player?key={token_hypixel}&uuid={uuid}").json()
    try:
        return req["player"]["socialMedia"]["links"]["DISCORD"]
    except Exception:
        if req["success"] == "true":
            return 0
        return


def return_uuid(pseudo):
    req = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{pseudo}").json()
    try:
        return req["id"]
    except Exception:
        # This Minecraft pseudo doesn't exist
        if req["errorMessage"] == f"Couldn't find any profile with name {pseudo}":
            return 0
        return


def return_guild(name):
    req = requests.get(f"{api_hypixel}guild?key={token_hypixel}&name={name}").json()
    try:
        return req["guild"]
    except Exception:
        return


def is_in_guild(uuid, g_name):
    guild = return_guild(g_name)
    if guild is None:
        return
    for member in guild["members"]:
        if member["uuid"] == uuid:
            return True
    return False


def check(pseudo, guild, discord):
    uuid = return_uuid(pseudo)
    if uuid == 0:
        return f"Il n'y a pas de compte Minecraft avec ce pseudo : {pseudo}"
    elif uuid is None:
        return "Something wrong happened"

    discord_mc = return_discord_hypixel(uuid)
    if discord_mc == 0:
        return "Vous n'avez pas entré de pseudo Discord sur le serveur Hypixel"
    elif not discord_mc == discord:
        return "Votre pseudo Discord ne correspond pas à celui entré sur le serveur Hypixel"
    elif discord_mc is None:
        return "Something wrong happened"

    test = is_in_guild(uuid, guild)
    if test:
        return True
    elif test is None:
        return f"Il n'y a pas de guilde avec ce nom : {guild}"
    return "Something very wrong happened"
