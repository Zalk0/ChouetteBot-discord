from aiohttp import ClientSession


async def get_last_update(session: ClientSession) -> str:
    """Récupère la date du dernier commit sur le dépôt principal de ChouetteBot."""
    async with session.get(
        "https://api.github.com/repos/Zalk0/chouettebot-discord/commits/main"
    ) as response:
        commit_infos = await response.json()
    return commit_infos["commit"]["author"]["date"][:10]
