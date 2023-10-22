from commands.skyblock import Skyblock
from commands.utils import latex, die_roll, ping, cheh, pin, delete


# List of commands to add to the command tree
def commands_list(tree, hypixel_guild):
    # List the commands
    commands = (
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
