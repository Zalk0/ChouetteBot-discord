import discord
import random


def commands_list(client, tree):

    # Make the roll command
    @tree.command(name="roll", description="Roll a die")
    async def die_roll(interaction: discord.Interaction):
        await interaction.response.send_message(f"{random.randint(1, 6)} \N{GAME DIE}")

    # Make the ping command
    @tree.command(name="ping", description="Test the ping of the bot")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! In {round(client.latency * 1000)}ms")

    # Make a cheh command
    @tree.command(name="cheh", description="Cheh somebody")
    async def cheh(interaction: discord.Interaction, user: discord.Member):
        cheh_gif = "https://tenor.com/view/cheh-true-cheh-gif-19162969"
        await interaction.response.send_message(f"Cheh {user.mention} {cheh_gif}")

    # Make a simple context menu application
    @tree.context_menu(name="Hello")
    async def hello(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(f"Hey! {interaction.user.mention}")

    # Make a context menu command to delete messages
    # @tree.context_menu(name="Delete until here")
    # async def delete(interaction: discord.Interaction, message: discord.Message):
    #     def is_msg(msg):
    #         return msg.id == message.id
    #     del_msg = await discord.TextChannel.purge(client, check=is_msg, bulk=True, reason="Admin used bulk delete")
    #     await interaction.response.send_message(f"{del_msg} messages deleted!", ephemeral=True)
    # exception: AttributeError: 'YoloBot' object has no attribute 'history'
