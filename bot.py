import discord

client = discord.Client()
client.run('MTA2MDI1MjY1MjI4MzM3OTg5NA.GIWIoq.U6SL91qCbXhsK06YnWoK30g9UP2ql881bRpVig')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')
