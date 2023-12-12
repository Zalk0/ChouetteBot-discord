import aiohttp
from dotenv import dotenv_values

api_hypixel = "https://api.hypixel.net/"
token_hypixel = dotenv_values()["HYPIXEL_KEY"]


async def fetch(session, url, params=None):
    async with session.get(url, params=params) as response:
        return await response.json()


async def return_discord_hypixel(session, uuid):
    response = await fetch(
        session, f"{api_hypixel}player", {"key": token_hypixel, "uuid": uuid}
    )
    try:
        return response["player"]["socialMedia"]["links"]["DISCORD"]
    except Exception:
        if response["success"] == "true":
            return 0
        return


async def return_uuid(session, pseudo):
    response = await fetch(
        session, f"https://api.mojang.com/users/profiles/minecraft/{pseudo}"
    )
    try:
        return response["id"]
    except Exception:
        # This Minecraft pseudo doesn't exist
        if (
            response["errorMessage"]
            == f"Couldn't find any profile with name {pseudo}"
        ):
            return 0
        return


async def return_guild(session, name):
    response = await fetch(
        session, f"{api_hypixel}guild", {"key": token_hypixel, "name": name}
    )
    try:
        return response["guild"]
    except Exception:
        return


async def is_in_guild(session, uuid, g_name):
    guild = await return_guild(session, g_name)
    if guild is None:
        return
    for member in guild["members"]:
        if member["uuid"] == uuid:
            return True
    return False


async def check(pseudo, guild, discord):
    async with aiohttp.ClientSession() as session:
        uuid = await return_uuid(session, pseudo)
        if uuid == 0:
            return (
                f"Il n'y a pas de compte Minecraft avec ce pseudo : {pseudo}"
            )
        elif uuid is None:
            return "Something wrong happened"

        discord_mc = await return_discord_hypixel(session, uuid)
        if discord_mc == 0:
            return "Vous n'avez pas entré de pseudo Discord sur le serveur Hypixel"
        elif not discord_mc == discord:
            return "Votre pseudo Discord ne correspond pas à celui entré sur le serveur Hypixel"
        elif discord_mc is None:
            return "Something wrong happened"

        test = await is_in_guild(session, uuid, guild)
        if test:
            return True
        elif test is None:
            return f"Il n'y a pas de guilde avec ce nom : {guild}"
        return "Something very wrong happened"
