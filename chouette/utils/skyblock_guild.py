from os import getenv

import aiohttp

from chouette.utils.skyblock import minecraft_uuid

api_hypixel = "https://api.hypixel.net/v2/"


async def fetch(session, url, params=None):
    """Effectue une requête GET asynchrone à l'URL spécifiée avec les paramètres donnés, sous forme JSON."""
    async with session.get(url, params=params) as response:
        return await response.json()


async def return_discord_hypixel(session, uuid, token_hypixel):
    """Récupère le pseudo Discord d'un joueur Hypixel avec l'API."""
    response = await fetch(session, f"{api_hypixel}player", {"key": token_hypixel, "uuid": uuid})
    try:
        return response["player"]["socialMedia"]["links"]["DISCORD"]
    except Exception:
        if response["success"] == "true":
            return 0
        return None


async def return_guild(session, name, token_hypixel):
    """Récupère les informations d'une guilde Hypixel avec l'API."""
    response = await fetch(session, f"{api_hypixel}guild", {"key": token_hypixel, "name": name})
    try:
        return response["guild"]
    except Exception:
        return None


async def is_in_guild(session, uuid, g_name, token_hypixel) -> bool | None:
    """Vérifie si un joueur est dans une guilde Hypixel."""
    guild = await return_guild(session, g_name, token_hypixel)
    if guild is None:
        return None
    return any(member["uuid"] == uuid for member in guild["members"])


async def check(pseudo, guild, discord):
    """Vérifie  des informations sur un joueur Minecraft.
    On vérifie si le pseudo Minecraft existe, si le pseudo Discord correspond à celui associé à Hypixel,
    et si le joueur est dans une guilde Hypixel."""
    token_hypixel = getenv("HYPIXEL_KEY")
    async with aiohttp.ClientSession() as session:
        uuid = await minecraft_uuid(session, pseudo)
        if uuid == 0:
            return f"Il n'y a pas de compte Minecraft avec ce pseudo : {pseudo}"
        if uuid is None:
            return "Something wrong happened"

        discord_mc = await return_discord_hypixel(session, uuid, token_hypixel)
        if discord_mc == 0:
            return "Vous n'avez pas entré de pseudo Discord sur le serveur Hypixel"
        if discord_mc != discord:
            return "Votre pseudo Discord ne correspond pas à celui entré sur le serveur Hypixel"
        if discord_mc is None:
            return "Something wrong happened"

        test = await is_in_guild(session, uuid, guild, token_hypixel)
        if test:
            return True
        if test is None:
            return f"Il n'y a pas de guilde avec ce nom : {guild}"
        return "Something very wrong happened"
