import discord
import discord.ext

# setting up the bot
intents = discord.Intents.all() 
# if you don't want all intents you can do discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# sync the slash command to your server
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=284980887634837504)) #guild id = server id
    # print "ready" in the console when the bot is ready to work
    print("Ready")

# make the slash command
@tree.command(name="ping", description="my ping")
async def slashing_commanding(int: discord.Interaction):    
    await int.response.send_message("Pong!")

# run the bot
client.run("MTA2MDI1MjY1MjI4MzM3OTg5NA.GIWIoq.U6SL91qCbXhsK06YnWoK30g9UP2ql881bRpVig")
