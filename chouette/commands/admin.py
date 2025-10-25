from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot


# Maybe add server admins later
async def is_admin(interaction: discord.Interaction[ChouetteBot]) -> bool:
    """Vérifie si l'utilisateur est un admin du bot.

    Args:
        interaction (discord.Interaction[ChouetteBot]): L'interaction Discord.

    Returns:
        bool: `True` si l'utilisateur est un admin du bot, `False` sinon.
    """
    return await interaction.client.is_team_member_or_owner(interaction.user)


@app_commands.check(is_admin)
@app_commands.command(name="whisper", description="Chuchotte un message")
async def whisper(interaction: discord.Interaction[ChouetteBot], message: str) -> None:
    """Fait chuchoter un message par le bot. Uniquement les admins du bot peuvent utiliser cette commande.

    Args:
        interaction (discord.Interaction[ChouetteBot]): L'interaction Discord.
        message (str): Le message à chuchoter.
    """
    await interaction.channel.send(f"{interaction.client.user.name} veut dire : {message}")
    await interaction.response.send_message("Commande réussie", ephemeral=True, delete_after=2)
