from aiohttp import ClientSession


async def get_last_update(session: ClientSession) -> str:
    """Récupère la date du dernier commit sur le dépôt principal de ChouetteBot.

    Args:
        session (ClientSession): La session HTTP aiohttp.

    Returns:
        str: La date du dernier commit au format 'YYYY-MM-DD'.
    """
    async with session.get(
        "https://api.github.com/repos/Zalk0/chouettebot-discord/commits/main"
    ) as response:
        commit_infos = await response.json()
    return commit_infos["commit"]["author"]["date"][:10]
