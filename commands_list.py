from typing import Tuple

import discord

from commands.skyblock import Skyblock
from commands.utils import latex, die_roll, ping, cheh, pin, delete


# List of commands to add to the command tree
async def commands_list(tree: discord.app_commands.CommandTree, hypixel_guild: discord.Guild):
    # List the commands
    commands: Tuple = (
        latex,
        die_roll,
        ping,
        cheh,
        pin,
        delete
    )

    # Add the commands
    for command in commands:
        tree.add_command(command)

    # Add the skyblock command group to my Hypixel guild
    tree.add_command(Skyblock(), guild=hypixel_guild)
