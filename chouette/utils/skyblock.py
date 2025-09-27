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
    """Charge les données du Skyblock à partir du disque."""
    return await data_read(SKYBLOCK_FILE)


async def save_skyblock(skyblock: dict) -> None:
    """Sauvegarde les données du Skyblock sur le disque."""
    await data_write(skyblock, SKYBLOCK_FILE)


async def minecraft_uuid(session: ClientSession, pseudo: str) -> tuple[bool, str]:
    """Retourne l'UUID d'un joueur Minecraft avec l'API Mojang."""
    async with session.get(
        f"https://api.mojang.com/users/profiles/minecraft/{pseudo}"
    ) as response:
        json: dict = await response.json()
        if response.status != 200:
            return False, json.get("errorMessage")
        return True, json.get("id")


async def hypixel_discord(player: dict) -> tuple[bool, str]:
    """Retourne le pseudo Discord lié à un compte Hypixel."""
    if not player.get("player").get("socialMedia", {}).get("links", {}).get("DISCORD", ""):
        return False, "Vous n'avez pas associé votre compte Discord à Hypixel"
    return True, player.get("player").get("socialMedia").get("links").get("DISCORD")


async def selected_profile(
    session: ClientSession, api_key: str, uuid: str
) -> tuple[bool, dict | str]:
    """Retourne le profil Skyblock sélectionné d'un joueur."""
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
) -> tuple[bool, dict | str]:
    """Retourne le profil Skyblock d'un joueur avec un nom spécifique."""
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
    """Retourne le profil d'un joueur Hypixel."""
    async with session.get(
        f"{HYPIXEL_API}player", params={"key": api_key, "uuid": uuid}
    ) as response:
        json: dict = await response.json()
        if response.status != 200:
            raise Exception("Error while fetching Hypixel player info")
        return json


async def get_stats(session, pseudo, uuid, hypixel_player, profile) -> dict[str, float]:
    """Retourne les statistiques d'un joueur Skyblock avec l'API."""
    info = profile.get("members").get(uuid)
    level: float = (info.get("leveling").get("experience")) / 100
    # TODO: new API for networth or use Altpapier/SkyHelper-Networth
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
        "skills": skills,
        "slayers": slayers,
        "level_cap": level_cap,
    }


async def pseudo_to_profile(
    client: ChouetteBot, discord_pseudo: str, pseudo: str, name: str | None
) -> dict | str:
    session = client.session

    """Retourne le profil d'un joueur Skyblock avec l'API."""
    uuid = await minecraft_uuid(session, pseudo)
    if not uuid[0]:
        # TODO: better handling
        return uuid[1]
    uuid = uuid[1]
    client.bot_logger.debug(f"L'UUID de {pseudo} est {uuid}")

    api_key = client.config.get("HYPIXEL_KEY")

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

    if name:
        profile = await get_profile(session, api_key, uuid, name)
    else:
        profile = await selected_profile(session, api_key, uuid)
    if not profile[0]:
        # TODO: better handling
        return profile[1]
    profile = profile[1]
    client.bot_logger.debug(f"Le profil {profile.get('cute_name')} a été trouvé")

    info = {uuid: {"discord": discord, "pseudo": pseudo, "profile": profile.get("cute_name")}}
    info.get(uuid).update(await get_stats(session, pseudo, uuid, player, profile))
    client.bot_logger.debug("Les stats ont bien été calculées")
    file_content = await load_skyblock()
    if file_content.get(uuid, {}).get("profile", "") != profile.get("profile_id"):
        file_content.update(info)
        await save_skyblock(file_content)
    return info.get(uuid)
