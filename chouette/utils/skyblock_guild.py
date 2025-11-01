from __future__ import annotations

from os import getenv

from aiohttp import ClientSession

from chouette.utils.skyblock import get_hypixel_player, hypixel_discord, minecraft_uuid

api_hypixel = "https://api.hypixel.net/v2/"


async def fetch(session, url, params=None):
    """Effectue une requête GET asynchrone à l'URL spécifiée avec les paramètres donnés, sous forme JSON."""
    async with session.get(url, params=params) as response:
        return await response.json()


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


async def check(session: ClientSession, pseudo, guild, discord):
    """Vérifie des informations sur un joueur Minecraft.
    On vérifie si le pseudo Minecraft existe, si le pseudo Discord correspond à celui associé à Hypixel,
    et si le joueur est dans une guilde Hypixel."""
    token_hypixel = getenv("HYPIXEL_KEY")
    uuid = await minecraft_uuid(session, pseudo)
    if not uuid[0]:
        return uuid[1]
    uuid = uuid[1]

    player = await get_hypixel_player(session, token_hypixel, uuid)
    discord_mc = await hypixel_discord(player)
    if not discord_mc[0]:
        return discord_mc[1]
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
