from discord import *

intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

#fixing
@client.event
async def ping(ctx):
    await ctx.reply("Pong !")

client.run('MTA2MDI1MjY1MjI4MzM3OTg5NA.GIWIoq.U6SL91qCbXhsK06YnWoK30g9UP2ql881bRpVig')