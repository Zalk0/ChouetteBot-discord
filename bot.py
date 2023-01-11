import inspect
import os
from datetime import time
import discord
from discord.utils import get
from discord.ext import tasks, commands

# setting up the client
intents = discord.Intents.all()
even_hours = [time(0), time(2), time(4), time(6), time(8), time(10),
              time(12), time(14), time(16), time(18), time(20), time(22)]


class AClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        activity = discord.Activity(type=discord.ActivityType.listening, name="Bring Me The Horizon")
        await client.change_presence(activity=activity, status=discord.Status.idle)
        if not self.synced:
            await tree.sync()
            self.synced = True
        if not self.added:
            self.added = True
        print(f"Logged in {self.user}!")


client = AClient()
tree = discord.app_commands.CommandTree(client)


# make the ping command
@tree.command(name="ping", description="You can test your ping here!")
async def slashing_commanding(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


# make a hello application for the bot
@tree.context_menu(name="Hello")
async def hello(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message("Hey!")


# Tasks for pinging @Dresseur pokémon hunting! @Gylfirst fix this
@tree.command(name="pokehunt", description="Command to launch pings for pokemons hunters")
async def poke(ctx):
    poke_ping.start(ctx)
    await ctx.response.send_message("La commande a bien été effectuée !", ephemeral=True)


@tasks.loop(time=even_hours)
async def poke_ping(ctx):
    dresseurs = get(ctx.guild.roles, id=791365470837800992)
    pokeball = client.get_emoji(697018415646507078)
    msg_poke = f"{dresseurs.mention} C'est l'heure d'attraper des pokémons {pokeball}"
    await client.get_channel(768554688425492560).send(msg_poke)


# Import token from file
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
with open(f"{module_dir}/token_discord", "r") as file:
    token = file.read()

# run the client
client.run(token, reconnect=True)
