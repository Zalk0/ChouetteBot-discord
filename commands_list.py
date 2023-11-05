from typing import Tuple

import discord

from commands.skyblock import Skyblock
from commands.utils import latex, die_roll, ping, cheh, pin, delete

# List the commands
commands_list: Tuple = (
    latex,
    die_roll,
    ping,
    cheh,
    pin,
    delete
)


# List of commands to add to the command tree
async def commands(tree: discord.app_commands.CommandTree, hypixel_guild: discord.Guild):
    # Add the commands to the Tree
    for command in commands_list:
        tree.add_command(command)

    # Add the Skyblock command group to my Hypixel guild
    tree.add_command(Skyblock(), guild=hypixel_guild)

    # Create a global commands error handler
    @tree.error
    async def on_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.BotMissingPermissions):
            bot_perms = ", ".join(error.missing_permissions)
            interaction.client.bot_logger.error(f"{interaction.client.user} is missing {bot_perms} "
                                                f"to do {interaction.command.name} in #{interaction.channel}")
            if len(error.missing_permissions) == 1:
                await interaction.response.send_message(f"I am missing this permission: {bot_perms}",
                                                        ephemeral=True)
            else:
                await interaction.response.send_message(f"I am missing these permissions: {bot_perms}",
                                                        ephemeral=True)
            return
        if isinstance(error, discord.app_commands.MissingPermissions):
            user_perms = ", ".join(error.missing_permissions)
            interaction.client.bot_logger.error(f"{interaction.user} is missing {user_perms} "
                                                f"to do {interaction.command.name} in #{interaction.channel}")
            if len(error.missing_permissions) == 1:
                await interaction.response.send_message(f"You are missing this permission: {user_perms}",
                                                        ephemeral=True)
            else:
                await interaction.response.send_message(f"You are missing these permissions: {user_perms}",
                                                        ephemeral=True)
            return
        await interaction.response.send_message(f"{error}\nThis error is not caught, please signal it!",
                                                ephemeral=True)
        interaction.client.bot_logger.error(error)
