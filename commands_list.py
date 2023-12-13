from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import discord

from commands.admin import whisper
from commands.misc import latex, die_roll, ping, cheh, pin, delete
from commands.skyblock import Skyblock

if TYPE_CHECKING:
    from bot import ChouetteBot

# List the commands
COMMANDS_LIST: Tuple = (
    latex,
    die_roll,
    ping,
    cheh,
    pin,
    delete,
    whisper,
)

SPACES = " " * 38


# List of commands to add to the command tree
async def commands(
    tree: discord.app_commands.CommandTree, hypixel_guild: discord.Guild
):
    # Add the commands to the Tree
    for command in COMMANDS_LIST:
        tree.add_command(command)

    # Add the Skyblock command group to my Hypixel guild
    tree.add_command(Skyblock(), guild=hypixel_guild)

    # Create a global commands error handler
    @tree.error
    async def on_command_error(
        interaction: discord.Interaction[ChouetteBot],
        error: discord.app_commands.AppCommandError,
    ):
        if isinstance(error, discord.app_commands.BotMissingPermissions):
            bot_perms = ", ".join(error.missing_permissions)
            interaction.client.bot_logger.error(
                f"{interaction.client.user} is missing {bot_perms} "
                f"to do {interaction.command.name} in #{interaction.channel}"
            )
            if len(error.missing_permissions) == 1:
                await interaction.response.send_message(
                    f"I am missing this permission: {bot_perms}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"I am missing these permissions: {bot_perms}",
                    ephemeral=True,
                )
            return
        if isinstance(error, discord.app_commands.MissingPermissions):
            user_perms = ", ".join(error.missing_permissions)
            interaction.client.bot_logger.error(
                f"{interaction.user} is missing {user_perms} "
                f"to do {interaction.command.name} in #{interaction.channel}"
            )
            if len(error.missing_permissions) == 1:
                await interaction.response.send_message(
                    f"You are missing this permission: {user_perms}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"You are missing these permissions: {user_perms}",
                    ephemeral=True,
                )
            return
        if isinstance(error, discord.app_commands.CheckFailure):
            interaction.client.bot_logger.error(
                f"{interaction.user} tried to do {interaction.command.name} "
                f"in #{interaction.channel}\n{SPACES}{error}"
            )
            await interaction.response.send_message(
                "You're not allowed to use this command!", ephemeral=True
            )
            return
        await interaction.response.send_message(
            f"{error}\nThis error is not caught, please signal it!",
            ephemeral=True,
        )
        interaction.client.bot_logger.error(error)
