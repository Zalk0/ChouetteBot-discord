import discord
from discord.utils import get
from discord.ext import tasks

# setting up the bot
intents = discord.Intents.all()

class aclient(discord.Client):
	def __init__(self):
		super().__init__(intents = intents)
		self.synced = False
		self.added = False

	async def on_ready(self):
		await self.wait_until_ready()
		if not self.synced:
			await tree.sync()
			self.synced = True
		if not self.added:
			self.added = True
		print(f"Logged in {self.user}!")
		
client = aclient()
tree = discord.app_commands.CommandTree(client)

# make the ping command
@tree.command(name="ping", description="You can test your ping here!")
async def slashing_commanding(int: discord.Interaction):
	await int.response.send_message("Pong!")

# make a hello application for the bot
@tree.context_menu(name="Hello")
async def hello(interaction: discord.Interaction, message: discord.Message):
	await interaction.response.send_message("Hey!")

# Tasks for pinging @Dresseur pokémon hunting! @Gylfirst fix this
@tree.command(name="start-pokemons", description="Command to launch pings for pokemons hunters")
async def poke(ctx):
	poke_ping.start(ctx)
@tasks.loop(hours=2)
async def poke_ping(ctx):
	Dresseurs = get(ctx.guild.roles, id=791365470837800992)
	await client.get_channel(768554688425492560).send(f"{Dresseurs.mention} C'est l'heure d'attraper des pokémons !")

# Import token from file
import inspect
import os
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
with open(f"{module_dir}/token_discord", "r") as file:
	token = file.read()

# run the bot
client.run(token)
