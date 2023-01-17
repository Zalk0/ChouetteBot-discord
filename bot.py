import commands
import discord
import inspect
import os
import responses
import tasks


# Create a class of the bot
class ChouetteBot(discord.Client):

    # Initialization when class is called
    def __init__(self):
        # Set intents for the bot
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.synced = False
        self.added = False

    # Wait until bot is ready
    async def on_ready(self):
        # Waits until internal cache is ready
        await self.wait_until_ready()

        # Import tasks
        tasks.tasks_list(self)

        # Import commands and sync
        command_tree = discord.app_commands.CommandTree(self)
        commands.commands_list(self, command_tree)
        if not self.synced:
            await command_tree.sync()
            self.synced = True
        if not self.added:
            self.added = True

        # Set activity of the bot
        activity = discord.Activity(type=discord.ActivityType.listening, name="Bring Me The Horizon")
        await self.change_presence(activity=activity, status=discord.Status.idle)

        # Check the number of servers the bot is a part of
        print(f"Number of servers I'm in : {len(self.guilds)}")

        # Prints in the console that the bot is ready
        print(f'{self.user} is now online and ready!')

    # Event when the bot receives a message
    async def on_message(self, message):
        # If the message is from a bot, ignore
        if message.author.bot:
            return

        # Stock the message's informations in variables
        username = str(message.author)
        user_msg = str(message.content)
        channel = message.channel

        # Do a log on the python console
        print(f'{username} said: "{user_msg}" ({channel})')

        # Call responses with message of the user and responds if necessary
        response = responses.responses(user_msg)
        if not response == '':
            await channel.send(response)
            print(f'{self.user} responded : {response}')


# Function to run the bot
def run_bot():

    # Import token from file
    module_path = inspect.getfile(inspect.currentframe())
    module_dir = os.path.realpath(os.path.dirname(module_path))
    with open(f"{module_dir}/token_discord", "r") as file:
        token = file.read()

    # Create an instance of the YoloBot class
    client = ChouetteBot()

    # Run the client with the token
    client.run(token, reconnect=True)
