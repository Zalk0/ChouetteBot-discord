import discord

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

@tree.context_menu(name="Hello")
async def hello(interaction: discord.Interaction, message: discord.message):
	await interaction.response.send_message("Hey!")

# run the bot
client.run("MTA2MDI1MjY1MjI4MzM3OTg5NA.GIWIoq.U6SL91qCbXhsK06YnWoK30g9UP2ql881bRpVig")
