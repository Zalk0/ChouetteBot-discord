import commands
import discord
import inspect
import os
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

        # Import commands and sync
        command_tree = discord.app_commands.CommandTree(self)
        commands.commands_list(self, command_tree)
        if not self.synced:
            await command_tree.sync()
            self.synced = True
        if not self.added:
            self.added = True

        # Import tasks
        tasks.tasks_list(self)

        # Set activity of the bot
        activity = discord.Activity(type=discord.ActivityType.listening, name="Bring Me The Horizon")
        await self.change_presence(activity=activity, status=discord.Status.idle)

        # Prints in the console that the bot is ready
        print(f'{self.user} is now online and ready!')

    # Event when the bot receives a message
    async def on_message(self, message):
        # If the message is from the bot ignore
        if message.author == self.user:
            return

        # Stock the message's informations in variables
        username = str(message.author)
        user_msg = str(message.content)
        channel = str(message.channel)

        # Do a log on the python console
        print(f'{username} said: "{user_msg}" ({channel})')


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
