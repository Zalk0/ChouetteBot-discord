from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot


# Check if user is an admin of the bot
# Maybe add server admins later
async def is_admin(interaction: discord.Interaction[ChouetteBot]):
    return await interaction.client.is_team_member_or_owner(interaction.user)


# Command to publish a message from admins by the bot
@app_commands.check(is_admin)
@app_commands.command(name="whisper", description="Chuchotte un message")
async def whisper(interaction: discord.Interaction[ChouetteBot], message: str):
    await interaction.channel.send(
        f"{interaction.client.user.name} veut dire : {message}"
    )
    await interaction.response.send_message("Commande réussie", ephemeral=True, delete_after=2)
