from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from chouette.commands.admin import whisper
from chouette.commands.birthdays import Birthday
from chouette.commands.misc import cheh, delete, die_roll, info, latex, pin, ping
from chouette.commands.skyblock import Skyblock

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot

# List the commands
COMMANDS_LIST: tuple = (
    cheh,
    delete,
    die_roll,
    info,
    latex,
    pin,
    ping,
    whisper,
)

SPACES = " " * 38


async def commands(client: ChouetteBot) -> None:
    """Ajoute les commandes à l'arbre des commandes.

    Args:
        client (ChouetteBot): L'instance du bot.
    """
    for command in COMMANDS_LIST:
        client.tree.add_command(command)

    # Add the Skyblock command group to my Hypixel guild
    client.tree.add_command(Skyblock(), guild=client.hypixel_guild)

    # Add the Birthday command group to my guild
    client.tree.add_command(Birthday(), guild=client.my_guild)

    # Create a global commands error handler
    @client.tree.error
    async def on_command_error(
        interaction: discord.Interaction[ChouetteBot], error: discord.app_commands.AppCommandError
    ) -> None:
        """Gère les erreurs lors de l'exécution des commandes.

        Args:
            interaction (discord.Interaction[ChouetteBot]): L'interaction qui a causé l'erreur.
            error (discord.app_commands.AppCommandError): L'erreur qui a été levée.
        """
        if interaction.response.is_done():
            return
        if isinstance(error, discord.app_commands.BotMissingPermissions):
            bot_perms = ", ".join(error.missing_permissions)
            interaction.client.bot_logger.error(
                f"{interaction.client.user} is missing {bot_perms} "
                f"to do /{interaction.command.qualified_name} in #{interaction.channel}"
            )
            if len(error.missing_permissions) == 1:
                await interaction.response.send_message(
                    f"Je n'ai pas cette permission : {bot_perms}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"Je n'ai pas cette permission : {bot_perms}",
                    ephemeral=True,
                )
            return
        if isinstance(error, discord.app_commands.MissingPermissions):
            user_perms = ", ".join(error.missing_permissions)
            interaction.client.bot_logger.error(
                f"{interaction.user} is missing {user_perms} "
                f"to do /{interaction.command.qualified_name} in #{interaction.channel}"
            )
            if len(error.missing_permissions) == 1:
                await interaction.response.send_message(
                    f"Vous n'avez pas ces permissions : {user_perms}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"Vous n'avez pas ces permissions : {user_perms}",
                    ephemeral=True,
                )
            return
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            interaction.client.bot_logger.error(
                f"{interaction.user} tried to use /{interaction.command.qualified_name} in "
                f"#{interaction.channel.name} but the command is in cooldown for {error.retry_after:.0f}s",
            )
            await interaction.response.send_message(
                f"Vous devez attendre {error.retry_after:.0f} secondes avant de réutiliser cette commande.",
                ephemeral=True,
            )
            return
        if isinstance(error, discord.app_commands.CheckFailure):
            interaction.client.bot_logger.error(
                f"{interaction.user} tried to do /{interaction.command.qualified_name} "
                f"in #{interaction.channel}\n{SPACES}{error}"
            )
            await interaction.response.send_message(
                "Vous n'êtes pas autorisé à exécuter cette commande !", ephemeral=True
            )
            return
        await interaction.response.send_message(
            f"{error}\nCette erreur n'a pas été récupérée, signalez la !",
            ephemeral=True,
        )
        interaction.client.bot_logger.error(error)
