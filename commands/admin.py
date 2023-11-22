from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands

if TYPE_CHECKING:
    from bot import ChouetteBot

# Command to publish a message from admins by the bot
@app_commands.command(name="wisper", description="Wisper an admin message")
async def wisper(interaction: discord.Interaction[ChouetteBot], message: str):
    if await interaction.client.is_team_member_or_owner(interaction.user):
        await interaction.channel.send(f"{interaction.client.user.name} wants so say this message: {message}")
        await interaction.response.send_message("Commande réussie", ephemeral=True)
