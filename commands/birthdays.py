from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

import discord
from discord import app_commands

from utils.birthdays import load_birthdays, save_birthdays

if TYPE_CHECKING:
    from bot import ChouetteBot


# Commande pour ajouter un anniversaire
@app_commands.command(
    name="add_birthday",
    description="Permit the user to register his birthday",
)
async def add_birthday(interaction: discord.Interaction[ChouetteBot]):
    date = datetime.now(tz=timezone.utc)
    user_id = str(interaction.user.id)
    birthdays = load_birthdays()
    birthdays.table[user_id]
    birthdays[user_id][interaction.user.name] = date
    save_birthdays(birthdays)
    await interaction.response.send_message("Anniversaire enregistré !", ephemeral=True)


# Commande pour supprimer un anniversaire
@app_commands.command(
    name="remove_birthday",
    description="Permit the user to delte his birthday",
)
async def remove_birthday(interaction: discord.Interaction[ChouetteBot]):
    user_id = str(interaction.user.id)
    birthdays = load_birthdays()
    if user_id in birthdays:
        del birthdays[user_id]
        save_birthdays(birthdays)
        await interaction.response.send_message("Anniversaire supprimé !")
    else:
        await interaction.response.send_message(
            "Vous n'avez pas d'anniversaire enregistré.", ephemeral=True
        )
