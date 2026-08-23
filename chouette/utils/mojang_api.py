from __future__ import annotations

from datetime import UTC, time
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from discord.ext import tasks

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot


class MojangAPIError(Exception):
    """Erreur de l'API Mojang."""

    def __init__(self, status: int, cause: str | None = None) -> None:
        self.message = f"HTTP Status code: {status}" + f", {cause}" if cause else ""


class MojangAPI:
    def __init__(self, client: ChouetteBot) -> None:
        self.client = client
        self.session = client.session
        self.minecraft_releases: list[str] = []
        self.update_minecraft_releases.start()

    async def pseudo_to_uuid(self, pseudo: str) -> str:
        """Retourne l'UUID d'un joueur Minecraft avec l'API Mojang.

        Args:
            pseudo (str): Le pseudo Minecraft du joueur.

        Returns:
            bool: `True` et l'UUID si le pseudo existe, `False` et un message d'erreur sinon.
        """
        async with self.session.get(
            f"https://api.mojang.com/users/profiles/minecraft/{pseudo}"
        ) as response:
            data: dict[str, Any] = await response.json()
        if data.get("id"):
            return data["id"]
        raise MojangAPIError(response.status, data.get("errorMessage"))

    async def set_minecraft_releases(self) -> None:
        async with self.session.get(
            "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        ) as response:
            if response.status in {HTTPStatus.OK, HTTPStatus.NOT_MODIFIED}:
                data: dict[str, Any] = await response.json()
                # We can't just set the item because references are used to access it
                self.minecraft_releases.clear()
                self.minecraft_releases.extend(
                    version["id"] for version in data["versions"] if version["type"] == "release"
                )
                return
        raise MojangAPIError(response.status)

    @tasks.loop(time=time(4, tzinfo=UTC))
    async def update_minecraft_releases(self) -> None:
        try:
            await self.set_minecraft_releases()
        except MojangAPIError as e:
            self.client.bot_logger.error(
                f"Error while updating cached Minecraft releases: {e.message}"
            )
