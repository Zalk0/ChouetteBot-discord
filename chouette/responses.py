from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.abc import Messageable

from chouette.utils.latex_render import latex_process

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot


async def responses(
    client: ChouetteBot,
    channel: Messageable,
    message: str,
    author: discord.User,
) -> tuple[str, bool]:
    """Vérifie si le message de l'utilisateur correspond à une réponse spécifique."""
    # Checks if a message ends with quoi
    if "".join(filter(str.isalpha, message)).lower().endswith("quoi"):
        return "**FEUR**", False

    # Checks if a message contains $$ to signify LaTeX expression
    if message.count("$") > 1:
        if (message.count("$") % 2) == 0:
            await channel.send(file=await latex_process(message))
            client.bot_logger.info(f'{client.user} responded to {author}: "equation.png"')
            return "", False
        return (
            "Nombre de $ impair, "
            "veuillez en mettre un nombre pair pour que je puisse afficher les équations LaTeX !",
            False,
        )

    # Add command to sync slash commands for team members and owner of the bot
    if message == f"{client.user.mention} sync":
        if await client.is_team_member_or_owner(author):
            try:
                await client.tree.sync()
                for guild in client.guilds:
                    await client.tree.sync(guild=guild)
                return "Les slashs commandes ont été synchronisées avec succès !", True
            except discord.app_commands.CommandSyncFailure as e:
                client.bot_logger.error(e)
                return str(e), True
        client.bot_logger.info(f"{author}, who isn't authorized, tried to sync the commands")

    # Return empty string if no condition is checked
    return "", False
