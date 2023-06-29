import discord
from dotenv import dotenv_values

import tasks
from commands_list import commands_list
from responses import responses


# Create a class of the bot
class ChouetteBot(discord.Client):

    # Initialization when class is called
    def __init__(self):
        # Set intents for the bot
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.synced = False

        # Associate the config to the bot
        self.config = dotenv_values()

    # Wait until bot is ready
    async def on_ready(self):
        # Waits until internal cache is ready
        await self.wait_until_ready()

        # Import tasks
        tasks.tasks_list(self)

        # Import commands and sync
        command_tree = discord.app_commands.CommandTree(self)
        commands_list(command_tree)
        if not self.synced:
            await command_tree.sync()
            self.synced = True

        # Set activity of the bot
        activity_type = {"playing": 0,
                         "streaming": 1,
                         "listening": 2,
                         "watching": 3,
                         "competing": 5}
        activity = discord.Activity(type=activity_type.get(self.config['BOT_ACTIVITY_TYPE']),
                                    name=self.config['BOT_ACTIVITY_NAME'])
        await self.change_presence(activity=activity, status=self.config['BOT_STATUS'])

        # Set up logging
        discord.utils.setup_logging()

        # Check the number of servers the bot is a part of
        print(f"Number of servers I'm in : {len(self.guilds)}")

        # Prints in the console that the bot is ready
        print(f'{self.user} is now online and ready!')

    # To react to messages sent in channels bot has access to
    async def on_message(self, message):
        # Ignore messages from bots including self
        if message.author.bot:
            return

        # Stock the message's informations in variables
        username = str(message.author)
        user_msg = str(message.content)
        channel = message.channel

        # Do a log on the Python console
        print(f'{username} said: "{user_msg}" ({channel}) in {message.guild.name}')

        # Call responses with message of the user and responds if necessary
        response = await responses(self, user_msg, channel)
        if not response == '':
            await channel.send(response)
            print(f'{self.user} responded : "{response}"')
