import logging
import os

import discord

import tasks
from commands_list import commands_list
from responses import responses


# Create a class of the bot
class ChouetteBot(discord.Client):

    # Initialization when class is called
    def __init__(self):
        # Associate the env variables to the bot
        self.config = os.environ

        # Define the bot debug log level
        self.bot_logger = logging.getLogger('bot')
        self.bot_logger.setLevel(logging.getLevelNamesMapping().get(self.config['LOG_LEVEL']) or logging.INFO)

        # Set intents for the bot
        intents = discord.Intents.all()

        # Set activity of the bot
        activity_type = {"playing": 0,
                         "streaming": 1,
                         "listening": 2,
                         "watching": 3,
                         "custom": 4,  # Idk what it is
                         "competing": 5}
        activity = discord.Activity(type=activity_type.get(self.config['BOT_ACTIVITY_TYPE']),
                                    name=self.config['BOT_ACTIVITY_NAME'])

        # Apply intents, activity and status to the bot
        super().__init__(intents=intents, activity=activity, status=self.config['BOT_STATUS'])

        # Used to check the first time the bot does the on_ready event
        self.first = True

    # Wait until bot is ready
    async def on_ready(self):
        # Waits until internal cache is ready
        await self.wait_until_ready()

        # Executed once when bot is ready
        if self.first:
            # Hypixel guild
            hypixel_guild = self.get_guild(int(self.config['HYPIXEL_GUILD_ID']))

            # Import and sync commands and import tasks
            command_tree = discord.app_commands.CommandTree(self)
            commands_list(command_tree, hypixel_guild)
            await command_tree.sync()
            await command_tree.sync(guild=hypixel_guild)
            tasks.tasks_list(self)
            self.first = False

        # Check the number of servers the bot is a part of
        self.bot_logger.info(f"Number of servers I'm in : {len(self.guilds)}")

        # Log in the console that the bot is ready
        self.bot_logger.info(f"{self.user} is now online and ready!")

    # To react to messages sent in channels bot has access to
    async def on_message(self, message: discord.Message):
        # Ignore messages from bots including self
        if message.author.bot:
            return

        # Stock the message's informations in variables
        username = str(message.author)
        user_msg = str(message.content)
        channel = message.channel

        # Do a log on the Python console
        if message.guild is not None:
            self.bot_logger.debug(f'{username} said: "{user_msg}" #{channel} in {message.guild.name}')
        else:
            self.bot_logger.debug(f'{username} said: "{user_msg}" in Direct Message')

        # Call responses with message of the user and responds if necessary
        response = await responses(self, channel, user_msg, username)
        if not response == '':
            await channel.send(response)
            self.bot_logger.info(f'{self.user} responded to {username}: "{response}"')
