from commands.skyblock import Skyblock
from commands.utils import latex, die_roll, ping, cheh, pin, delete


# List of commands to add to the command tree
def commands_list(tree, client):
    # Add the commands
    tree.add_command(latex)
    tree.add_command(die_roll)
    tree.add_command(ping)
    tree.add_command(cheh)
    tree.add_command(pin)
    tree.add_command(delete)

    # Add the skyblock command group to my Hypixel guild
    # hypixel_guild = client.get_guild(int(client.config['HYPIXEL_GUILD_ID']))
    tree.add_command(Skyblock())
