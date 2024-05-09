from pathlib import Path

from aiohttp import ClientSession

from chouette.utils.data_io import data_read, data_write

SKYBLOCK_FILE = Path("data", "skyblock.toml")
HYPIXEL_API = "https://api.hypixel.net/v2/"


async def load_skyblock() -> dict:
    """Load Skyblock data from disk."""
    return await data_read(SKYBLOCK_FILE)


async def save_skyblock(skyblock: dict) -> None:
    """Save Skyblock data to disk."""
    await data_write(skyblock, SKYBLOCK_FILE)


async def minecraft_uuid(session: ClientSession, pseudo: str) -> tuple[bool, str]:
    """Return player UUID from Mojang Minecraft API."""
    async with session.get(
        f"https://api.mojang.com/users/profiles/minecraft/{pseudo}"
    ) as response:
        json: dict = await response.json()
        if response.status != 200:
            return False, json.get("errorMessage")
        return True, json.get("id")


async def selected_profile(
    session: ClientSession, api_key: str, uuid: str
) -> tuple[bool, dict | str]:
    """Return selected Skyblock profile of a player."""
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
    """Return specified Skyblock profile of a player."""
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


async def get_stats(session, pseudo, uuid, profile):
    info = profile.get("members").get(uuid)
    level: float = (info.get("leveling").get("experience")) / 100
    async with session.get(f"https://sky.shiiyu.moe/api/v2/profile/{pseudo}") as response:
        networth: float = (
            (await response.json())
            .get("profiles")
            .get(profile.get("profile_id"))
            .get("data")
            .get("networth")
            .get("networth")
        )
    skills: dict[str, float] = {
        "farming": info.get("experience_skill_farming"),
        "mining": info.get("experience_skill_mining"),
        "foraging": info.get("experience_skill_foraging"),
        "fishing": info.get("experience_skill_fishing"),
        "carpentry": info.get("experience_skill_carpentry"),
        "taming": info.get("experience_skill_taming"),
        "combat": info.get("experience_skill_combat"),
        "alchemy": info.get("experience_skill_alchemy"),
        "enchanting": info.get("experience_skill_enchanting"),
        "dungeoneering": info.get("dungeons").get("dungeon_types").get("catacombs").get("experience")
    }
    slayer = info.get("slayer_bosses")
    slayers: dict[str, float] = {
        "zombie": slayer.get("zombie").get("xp"),
        "spider": slayer.get("spider").get("xp"),
        "wolf": slayer.get("wolf").get("xp"),
        "enderman": slayer.get("enderman").get("xp"),
        "blaze": slayer.get("blaze").get("xp"),
        "vampire": slayer.get("vampire").get("xp"),
    }
    return {"level": level, "networth": networth, "skills": skills, "slayers": slayers}


async def pseudo_to_profile(
    session: ClientSession, api_key: str, pseudo: str, name: str | None
) -> str:
    uuid = await minecraft_uuid(session, pseudo)
    if not uuid[0]:
        # TODO: better handling
        return uuid[1]
    uuid = uuid[1]
    if name:
        profile = await get_profile(session, api_key, uuid, name)
    else:
        profile = await selected_profile(session, api_key, uuid)
    if not profile[0]:
        # TODO: better handling
        return profile[1]
    profile = profile[1]
    info = {uuid: {"discord": "", "pseudo": pseudo, "profile": profile.get("profile_id")}}
    info.get(uuid).update(await get_stats(session, pseudo, uuid, profile))
    # TODO
