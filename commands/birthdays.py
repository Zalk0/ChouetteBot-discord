from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from discord import Interaction, app_commands
from tomlkit import table

from utils.birthdays import (
    check_date,
    datetime_to_timestamp,
    load_birthdays,
    save_birthdays,
)

if TYPE_CHECKING:
    from bot import ChouetteBot


class InvalidBirthdayDate(app_commands.AppCommandError):
    pass


# Define command group based on the Group class
class Birthday(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(name="birthday", description="Commandes pour gérer les anniversaires")

    async def on_error(
        self, interaction: Interaction[ChouetteBot], error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, InvalidBirthdayDate):
            interaction.client.bot_logger.info(
                f"{interaction.user} entered an invalid date as his birthday"
            )
            await interaction.response.send_message(
                "Vous n'avez pas entré une date d'anniversaire valide", ephemeral=True
            )

    # Make a command to add a birthday
    @app_commands.command(
        name="add",
        description="Permet d'enregistrer son anniversaire",
    )
    @app_commands.describe(day="Nombre entier", month="Nombre entier", year="Nombre entier")
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

    # Make a command to modify the birthday
    @app_commands.command(
        name="modify",
        description="Permet de modifier son anniversaire enregistré",
    )
    @app_commands.describe(day="Nombre entier", month="Nombre entier", year="Nombre entier")
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

    # Make a command to remove the birthday
    @app_commands.command(
        name="remove",
        description="Permet de supprimer son anniversaire enregistré",
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

    # Make a command to list all birthdays listed in database, sorted by date
    @app_commands.command(
        name="list",
        description="Liste les anniversaires enregistrés",
    )
    async def list(self, interaction: Interaction[ChouetteBot]):
        msg = f"Voici les anniversaires de {interaction.guild.name}\n"
        birthdays = sorted(
            (await load_birthdays()).items(), key=lambda x: x[1].get("birthday").replace(4)
        )
        if not birthdays:
            await interaction.response.send_message(msg + "\nListe des anniversaires vide")
            return
        msg += "```"
        next_birthday: date = None
        for user_id, info in birthdays:
            birthday: date = info.get("birthday")
            if not next_birthday and date.today().replace(birthday.year) < birthday:
                next_birthday = birthday.replace(date.today().year)
            name = interaction.guild.get_member(int(user_id)).display_name
            if len(name) > 25:
                name = name[:22] + "..."
            if len(name) < 25:
                name = name + (25 - len(name)) * " "
            msg += f"{name} : {birthday.day}/{birthday.month}\n"
        if not next_birthday:
            if (
                birthdays[0][1].get("birthday").day == 29
                and birthdays[0][1].get("birthday").month == 2
            ):
                next_birthday = (
                    birthdays[0][1].get("birthday").replace(date.today().year + 1, 3, 1)
                )
            else:
                next_birthday = birthdays[0][1].get("birthday").replace(date.today().year + 1)
        msg += "```"
        msg += f"Le prochain anniversaire est {await datetime_to_timestamp(next_birthday)}."
        await interaction.response.send_message(msg)
