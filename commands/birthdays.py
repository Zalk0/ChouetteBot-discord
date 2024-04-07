from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from discord import Interaction, app_commands
from tomlkit import table

from utils.birthdays import check_date, load_birthdays, save_birthdays

if TYPE_CHECKING:
    from bot import ChouetteBot


class InvalidBirthdayDate(app_commands.AppCommandError):
    pass


# Define command group based on the Group class
class Birthday(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(name="birthday", description="Birthday management related commands")

    async def on_error(
        self, interaction: Interaction[ChouetteBot], error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, InvalidBirthdayDate):
            interaction.client.bot_logger.info(
                f"{interaction.user} entered an invalid date as his birthday"
            )
            await interaction.response.send_message(
                "You did not enter a valid birthday", ephemeral=True
            )

    # Commande pour ajouter un anniversaire
    @app_commands.command(
        name="add",
        description="Permit the user to register his birthday",
    )
    async def add(
        self, interaction: Interaction[ChouetteBot], day: int, month: int, year: int | None
    ):
        try:
            birth_date = await check_date(day, month, year)
        except ValueError as e:
            raise InvalidBirthdayDate() from e
        user_id = str(interaction.user.id)
        birthdays = await load_birthdays()
        if user_id not in birthdays:
            user_info = table()
            user_info["name"] = interaction.user.name
            user_info["birthday"] = birth_date
            birthdays.update({user_id: user_info})
            await save_birthdays(birthdays)
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
        self, interaction: Interaction[ChouetteBot], day: int, month: int, year: int | None
    ):
        try:
            birth_date = await check_date(day, month, year)
        except ValueError as e:
            raise InvalidBirthdayDate() from e
        user_id = str(interaction.user.id)
        birthdays = await load_birthdays()
        if user_id in birthdays:
            user_info = table()
            user_info["name"] = interaction.user.name
            user_info["birthday"] = birth_date
            birthdays.update({user_id: user_info})
            await save_birthdays(birthdays)
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
    async def remove(self, interaction: Interaction[ChouetteBot]):
        user_id = str(interaction.user.id)
        birthdays = await load_birthdays()
        if user_id in birthdays:
            birthdays.pop(user_id)
            await save_birthdays(birthdays)
            await interaction.response.send_message("Anniversaire supprimé !", ephemeral=True)
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
    async def list(self, interaction: Interaction[ChouetteBot]):
        msg = f"Voici les anniversaires de {interaction.guild.name}\n```"
        birthdays = sorted(
            (await load_birthdays()).items(), key=lambda x: x[1].get("birthday").replace(4)
        )
        for user_id, info in birthdays:
            birthday: date = info.get("birthday")
            msg += (
                f"{interaction.guild.get_member(int(user_id)).display_name}: "
                f"{birthday.day}/{birthday.month}\n"
            )
        msg += "```"
        await interaction.response.send_message(msg)
