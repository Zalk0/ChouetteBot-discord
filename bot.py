import logging

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
        self.first = True

        # Associate the config to the bot
        self.config = dotenv_values()

    # Wait until bot is ready
    async def on_ready(self):
        # Waits until internal cache is ready
        await self.wait_until_ready()

        # Hypixel guild
        hypixel_guild = self.get_guild(int(self.config['HYPIXEL_GUILD_ID']))

        # Import and sync commands and import tasks
        command_tree = discord.app_commands.CommandTree(self)
        commands_list(command_tree, hypixel_guild)
        if self.first:
            await command_tree.sync()
            await command_tree.sync(guild=hypixel_guild)
            tasks.tasks_list(self)
            self.first = False

        # Set activity of the bot
        activity_type = {"playing": 0,
                         "streaming": 1,
                         "listening": 2,
                         "watching": 3,
                         "competing": 5}
        activity = discord.Activity(type=activity_type.get(self.config['BOT_ACTIVITY_TYPE']),
                                    name=self.config['BOT_ACTIVITY_NAME'])
        await self.change_presence(activity=activity, status=self.config['BOT_STATUS'])

        # Check the number of servers the bot is a part of
        logging.info(f"Number of servers I'm in : {len(self.guilds)}")

        # Log in the console that the bot is ready
        logging.info(f"{self.user} is now online and ready!")

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
        if message.guild is not None:
            logging.info(f'{username} said: "{user_msg}" #{channel} in {message.guild.name}')
        else:
            logging.info(f'{username} said: "{user_msg}" in Direct Message')

        # Call responses with message of the user and responds if necessary
        response = await responses(self, user_msg, channel)
        if not response == '':
            await channel.send(response)
            logging.info(f'{self.user} responded : "{response}"')
