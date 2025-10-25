from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from aiohttp import ClientSession

from chouette.utils.data_io import data_read, data_write

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot

SKYBLOCK_FILE = Path("data", "skyblock.toml")
HYPIXEL_API = "https://api.hypixel.net/v2/"


async def load_skyblock() -> dict:
    """Charge les données du Skyblock à partir du disque.

    Returns:
        dict: Les données du Skyblock.
    """
    return await data_read(SKYBLOCK_FILE)


async def save_skyblock(skyblock: dict) -> None:
    """Sauvegarde les données du Skyblock sur le disque.

    Args:
        skyblock (dict): Les données du Skyblock à sauvegarder.
    """
    await data_write(skyblock, SKYBLOCK_FILE)


async def minecraft_uuid(session: ClientSession, pseudo: str) -> tuple[bool, str | None]:
    """Retourne l'UUID d'un joueur Minecraft avec l'API Mojang.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        pseudo (str): Le pseudo Minecraft du joueur.

    Returns:
        tuple[bool, str | None]: `True` et l'UUID si le pseudo existe, `False` et un message d'erreur sinon.
    """
    async with session.get(
        f"https://api.mojang.com/users/profiles/minecraft/{pseudo}"
    ) as response:
        json: dict = await response.json()
        if response.status != 200:
            return False, json.get("errorMessage")
        return True, json.get("id")


async def hypixel_discord(player: dict) -> tuple[bool, str]:
    """Retourne le pseudo Discord lié à un compte Hypixel.

    Args:
        player (dict): Les données du joueur Hypixel.

    Returns:
        tuple[bool, str]: `True` et le pseudo Discord si le compte est lié, `False` et un message d'erreur sinon.
    """
    if not player.get("player").get("socialMedia", {}).get("links", {}).get("DISCORD", ""):
        return False, "Vous n'avez pas associé votre compte Discord à Hypixel"
    return True, player.get("player").get("socialMedia").get("links").get("DISCORD")


async def selected_profile(
    session: ClientSession, api_key: str, uuid: str
) -> tuple[bool, dict | str | None]:
    """Retourne le profil Skyblock sélectionné d'un joueur.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        api_key (str): La clé API Hypixel.
        uuid (str): L'UUID du joueur.

    Returns:
        tuple[bool, dict | str | None]: Le profil Skyblock sélectionné du joueur ou un message d'erreur.
    """
    async with session.get(
        f"{HYPIXEL_API}skyblock/profiles", params={"key": api_key, "uuid": uuid}
    ) as response:
        json: dict = await response.json()
        if response.status != 200:
            return False, json.get("cause")
        profiles = json.get("profiles")
        for profile in profiles:
            if profile.get("selected"):
                if profile.get("game_mode") == "bingo":
                    return False, "Bingo profile selected"
                return True, profile
        return False, json.get("cause") if not json.get("success") else "No profile"


async def get_profile(
    session: ClientSession, api_key: str, uuid: str, name: str
) -> tuple[bool, dict | str | None]:
    """Retourne le profil Skyblock d'un joueur avec un nom spécifique.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        api_key (str): La clé API Hypixel.
        uuid (str): L'UUID du joueur.
        name (str): Le nom du profil Skyblock.

    Returns:
        tuple[bool, dict | str | None]: `True` et le profil Skyblock si trouvé, `False` et un message d'erreur sinon.
    """
    async with session.get(
        f"{HYPIXEL_API}skyblock/profiles", params={"key": api_key, "uuid": uuid}
    ) as response:
        json: dict = await response.json()
        if response.status != 200:
            return False, json.get("cause")
        profiles = json.get("profiles")
        for profile in profiles:
            if profile.get("cute_name") == name:
                return True, profile
        return False, "No profile with this name"


async def get_hypixel_player(session: ClientSession, api_key: str, uuid: str) -> dict:
    """Retourne les informations d'un joueur Hypixel.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        api_key (str): La clé API Hypixel.
        uuid (str): L'UUID du joueur.

    Raises:
        Exception: Une exception est levée en cas d'erreur lors de la récupération des informations du joueur.

    Returns:
        dict: Les informations du joueur Hypixel.
    """
    async with session.get(
        f"{HYPIXEL_API}player", params={"key": api_key, "uuid": uuid}
    ) as response:
        json: dict = await response.json()
        if response.status != 200:
            raise Exception("Error while fetching Hypixel player info")
        return json


async def get_player_networth(
    minecraft_uuid: str, profile_uuid: str, session: ClientSession
) -> dict:
    """Retourne le networth d'un joueur Skyblock avec l'API de SkyCrypt.

    Args:
        minecraft_uuid (str): UUID Minecraft du joueur.
        profile_uuid (str): UUID du profil Skyblock du joueur.

    Returns:
        dict: Dictionnaire contenant le networth du joueur.
    """

    API_URL = "https://sky.shiiyu.moe/api/networth/{MC_UUID}/{PROFILE_UUID}"
    response = await session.get(API_URL.format(MC_UUID=minecraft_uuid, PROFILE_UUID=profile_uuid))
    if response.status != 200:
        return {
            "error": f"Failed to retrieve networth | status code: {response.status} | {await response.text()}"
        }
    return await response.json()


async def get_stats(
    session: ClientSession, uuid: str, hypixel_player: dict, profile: dict
) -> dict[str, float | tuple[float, ...] | tuple[int, ...]]:
    """Retourne les statistiques d'un joueur Skyblock avec l'API.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        uuid (str): L'UUID du joueur.
        hypixel_player (dict): Les informations du joueur Hypixel.
        profile (dict): Le profil Skyblock du joueur.

    Returns:
        dict[str, float | tuple[float, ...] | tuple[int, ...]]: Les statistiques du joueur Skyblock.
    """

    info = profile.get("members").get(uuid)
    level: float = (info.get("leveling").get("experience")) / 100
    networth: dict | int = (
        await get_player_networth(
            minecraft_uuid=uuid, profile_uuid=profile.get("profile_id"), session=session
        )
    ).get("networth", 0)
    if networth != 0:
        networth: float = networth["nonCosmetic"]["networth"]

    skill = info.get("player_data").get("experience")
    skills: tuple[float, float, float, float, float, float, float, float, float, float] = (
        skill.get("SKILL_FISHING", 0),
        skill.get("SKILL_ALCHEMY", 0),
        skill.get("SKILL_MINING", 0),
        skill.get("SKILL_FARMING", 0),
        skill.get("SKILL_ENCHANTING", 0),
        skill.get("SKILL_TAMING", 0),
        skill.get("SKILL_FORAGING", 0),
        skill.get("SKILL_CARPENTRY", 0),
        skill.get("SKILL_COMBAT", 0),
        info.get("dungeons").get("dungeon_types").get("catacombs").get("experience", 0),
    )
    slayer = info.get("slayer").get("slayer_bosses")
    slayers: tuple[int, int, int, int, int, int] = (
        slayer.get("zombie", {}).get("xp", 0),
        slayer.get("spider", {}).get("xp", 0),
        slayer.get("wolf", {}).get("xp", 0),
        slayer.get("enderman", {}).get("xp", 0),
        slayer.get("blaze", {}).get("xp", 0),
        slayer.get("vampire", {}).get("xp", 0),
    )
    level_cap: tuple[int, int] = (
        info.get("jacobs_contest", {}).get("perks", {}).get("farming_level_cap", 0),
        hypixel_player.get("player").get("achievements", {}).get("skyblock_domesticator", 0),
    )
    return {
        "level": level,
        "networth": networth,
        "skills": skills,
        "slayers": slayers,
        "level_cap": level_cap,
    }


async def pseudo_to_profile(
    client: ChouetteBot, discord_pseudo: str, pseudo: str, profile_name: str | None
) -> dict | str | None:
    """Retourne le profil d'un joueur Skyblock avec l'API.

    Args:
        client (ChouetteBot): Le client ChouetteBot.
        discord_pseudo (str): Le pseudo Discord du joueur.
        pseudo (str): Le pseudo Minecraft du joueur.
        profile_name (str | None): Le nom du profil Skyblock du joueur.

    Returns:
        dict | str | None: Les informations du profil Skyblock ou un message d'erreur.
    """
    session: ClientSession = client.session
    uuid = await minecraft_uuid(session, pseudo)
    if not uuid[0]:
        # TODO: better handling
        return uuid[1]
    uuid = uuid[1]
    client.bot_logger.debug(f"L'UUID de {pseudo} est {uuid}")

    api_key = client.config.get("HYPIXEL_KEY")
    if not api_key:
        client.bot_logger.error("La clé API Hypixel n'est pas configurée.")
        return "La clé API Hypixel n'est pas configurée."

    player = await get_hypixel_player(session, api_key, uuid)
    discord = await hypixel_discord(player)
    if not discord[0]:
        # TODO: better handling
        return discord[1]
    discord = discord[1]
    if discord != discord_pseudo:
        if discord.lower() == discord_pseudo:
            return (
                "Vous avez entré le bon pseudo Discord sur Hypixel "
                "mais il contient des majuscules !"
            )
        if not discord.islower():
            return "Le pseudo Discord entré sur Hypixel contient des majuscules !"
        return "Votre pseudo Discord ne correspond pas à celui entré sur le serveur Hypixel"
    client.bot_logger.debug("Les pseudos Discord correspondent")

    if profile_name:
        profile = await get_profile(session, api_key, uuid, profile_name)
    else:
        profile = await selected_profile(session, api_key, uuid)
    if not profile[0]:
        # TODO: better handling
        return profile[1]
    profile = profile[1]
    client.bot_logger.debug(f"Le profil {profile.get('cute_name')} a été trouvé")

    info = {uuid: {"discord": discord, "pseudo": pseudo, "profile": profile.get("cute_name")}}
    info.get(uuid).update(await get_stats(session, uuid, player, profile))
    client.bot_logger.debug("Les stats ont bien été calculées")
    file_content = await load_skyblock()
    if file_content.get(uuid, {}).get("profile", "") != profile.get("profile_id"):
        file_content.update(info)
        await save_skyblock(file_content)
    return info.get(uuid)
