import random

import discord

from latex_render import latex_render


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
        # Check if the user to cheh is the bot or the user sending the command
        if user == client.user:
            await interaction.response.send_message("Vous ne pouvez pas me **Cheh** !")
        elif user == interaction.user:
            await interaction.response.send_message("**FEUR**")
        else:
            cheh_gif = "https://tenor.com/view/cheh-true-cheh-gif-19162969"
            await interaction.response.send_message(f"Cheh {user.mention}")
            await interaction.channel.send(cheh_gif)

    # Make a simple context menu application
    @tree.context_menu(name="Hello")
    async def hello(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(f"Hey! {interaction.user.mention}")

    # Make a context menu command to delete messages
    # @tree.context_menu(name="Delete until here")
    # async def delete(interaction: discord.Interaction, message: discord.Message):
    #     if not interaction.permissions.manage_messages:
    #         await interaction.response.send_message(f"Vous n'avez pas la permission de gérer les messages !", ephemeral=True)
    #         return
    #     await interaction.response.defer(ephemeral=True, thinking=True)
    #     last_id = interaction.channel.last_message_id
    #     def is_msg(msg):
    #         if msg.id <= last_id:
    #             return msg.id >= message.id
    #     del_msg = await message.channel.purge(check=is_msg, reason="Admin used bulk delete")
    #     await interaction.followup.send(f"{len(del_msg)} messages supprimés !")

    # Make a LaTeX command
    @tree.command(name="latex", description="Renders LaTeX equation")
    async def latex(interaction: discord.Interaction, equation: str):
        await interaction.response.send_message(file=await latex_render(equation))
