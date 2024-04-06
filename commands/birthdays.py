from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from tomlkit import table

from utils.birthdays import check_year_value, load_birthdays, save_birthdays

if TYPE_CHECKING:
    from bot import ChouetteBot


# Define command group based on the Group class
class Birthday(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(name="birthday", description="Birthday management related commands")

    # Commande pour ajouter un anniversaire
    @app_commands.command(
        name="add",
        description="Permit the user to register his birthday",
    )
    async def add(
        self,
        interaction: discord.Interaction[ChouetteBot],
        day: int,
        month: int,
        year: int | None,
    ):
        try:
            year = check_year_value(year)
            birth_date = date(year, month, day)
        except ValueError:
            pass
        user_name = str(interaction.user.name)
        user_id = str(interaction.user.id)
        birthdays = load_birthdays()
        if user_id not in birthdays:
            user_info = table()
            user_info["name"] = user_name
            user_info["birthday"] = birth_date
            birthdays.update({user_id: user_info})
            save_birthdays(birthdays)
            await interaction.response.send_message("Anniversaire enregistré !", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Vous avez déjà un anniversaire enregistré.\n"
                "Vous pouvez le supprimer avec la commande `/birthday remove`\n"
                "Vous pouvez aussi le modifier avec la commande `/birthday modify`",
                ephemeral=True,
            )

    # Commande pour modifier un anniversaire
    @app_commands.command(
        name="modify",
        description="Permit the user to modify his birthday",
    )
    async def modify(
        self,
        interaction: discord.Interaction[ChouetteBot],
        day: int,
        month: int,
        year: int | None,
    ):
        try:
            year = check_year_value(year)
            birth_date = date(year, month, day)
        except ValueError:
            pass
        user_name = str(interaction.user.name)
        user_id = str(interaction.user.id)
        birthdays = load_birthdays()
        if user_id in birthdays:
            user_info = table()
            user_info["name"] = user_name
            user_info["birthday"] = birth_date
            birthdays.update({user_id: user_info})
            save_birthdays(birthdays)
            await interaction.response.send_message("Anniversaire modifié !", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Vous n'avez pas d'anniversaire enregistré.\n"
                "Vous pouvez l'ajouter avec la commande `/birthday add`",
                ephemeral=True,
            )

    # Commande pour supprimer un anniversaire
    @app_commands.command(
        name="remove",
        description="Permit the user to delete his birthday",
    )
    async def remove(self, interaction: discord.Interaction[ChouetteBot]):
        user_id = str(interaction.user.id)
        birthdays = load_birthdays()
        if user_id in birthdays:
            del birthdays[user_id]
            save_birthdays(birthdays)
            await interaction.response.send_message("Anniversaire supprimé !")
        else:
            await interaction.response.send_message(
                "Vous n'avez pas d'anniversaire enregistré."
                "Vous pouvez l'ajouter avec la commande `/birthday add`",
                ephemeral=True,
            )

    @app_commands.command(
        name="list",
        description="List saved birthdays",
    )
    async def list(self, interaction: discord.Interaction[ChouetteBot]):
        msg = "```"
        birthdays = load_birthdays()
        for birthday in birthdays:
            birth_date: date = birthdays.get(birthday).get("birthday")
            msg += (
                f"{birthdays.get(birthday).get('name')}: "
                f"{birth_date.day}/{birth_date.month}\n"
            )
        msg += "```"
        await interaction.response.send_message(msg)
