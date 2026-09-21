from datetime import date
from http import HTTPStatus

from aiohttp import ClientSession


class GitHubAPIError(Exception):
    """Erreur de l'API GitHub."""

    def __init__(self, status: int, cause: str | None = None) -> None:
        super().__init__(f"HTTP Status code: {status}" + f", {cause}" if cause else "")


async def get_last_update(session: ClientSession) -> date:
    """Récupère la date du dernier commit sur le dépôt principal de ChouetteBot.

    Args:
        session (ClientSession): La session HTTP aiohttp.

    Returns:
        date: La date du dernier commit.
    """
    async with session.get(
        "https://api.github.com/repos/Zalk0/chouettebot-discord/commits/main"
    ) as response:
        commit_infos: dict = await response.json()
        if response.status != HTTPStatus.OK:
            raise GitHubAPIError(response.status, commit_infos.get("message"))
    return date.fromisoformat(commit_infos["commit"]["author"]["date"][:10])
