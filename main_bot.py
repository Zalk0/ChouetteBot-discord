import discord
from discord.ext import tasks, commands

# setting up the bot
intents=discord.Intents.all()

class abot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix='!', intents = intents)

	async def on_ready(self):
		print(f"Logged in {self.user}!")
		
bot = abot()

@bot.command(name="del")
async def delete(ctx, limit: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    await ctx.send(f"Deleted {limit} messages", delete_after=5)

@bot.command()
async def testhi(ctx):
    testing.start(ctx)

@tasks.loop(hours=1)
async def testing(ctx):
    await ctx.send('Hi!', delete_after=5)

# Import token from file
import inspect
import os
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
with open(f"{module_dir}/token_discord", "r") as file:
	token = file.read()

# run the bot
bot.run(token, reconnect=True)
