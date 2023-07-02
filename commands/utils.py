import random

import discord
from discord import app_commands

from src.latex_render import latex_render


# Make a LaTeX command
@app_commands.command(name="latex", description="Render a LaTeX equation")
async def latex(interaction: discord.Interaction, equation: str):
    await interaction.response.send_message(file=await latex_render(equation))


# Make the roll command
@app_commands.command(name="roll", description="Roll a die")
async def die_roll(interaction: discord.Interaction):
    await interaction.response.send_message(f"{random.randint(1, 6)} \N{GAME DIE}")


# Make the ping command
@app_commands.command(name="ping", description="Test the ping of the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! In {round(interaction.client.latency * 1000)}ms")


# Make a cheh command
@app_commands.command(name="cheh", description="Cheh somebody")
async def cheh(interaction: discord.Interaction, user: discord.Member):
    # Check if the user to cheh is the bot or the user sending the command
    if user == interaction.client.user:
        await interaction.response.send_message("Vous ne pouvez pas me **Cheh** !")
    elif user == interaction.user:
        await interaction.response.send_message("**FEUR**")
    else:
        cheh_gif = "https://tenor.com/view/cheh-true-cheh-gif-19162969"
        await interaction.response.send_message(f"**Cheh** {user.mention}")
        await interaction.channel.send(cheh_gif)


# Make a simple context menu application to pin/unpin
@app_commands.context_menu(name="Pin/Unpin")
async def pin(interaction: discord.Interaction, message: discord.Message):
    if message.pinned:
        await message.unpin()
        await interaction.response.send_message("The message has been unpinned!", ephemeral=True)
    else:
        await message.pin()
        await interaction.response.send_message("The message has been pinned!", ephemeral=True)


# Make a context menu command to delete messages
# TODO Change permission management to use built-in discord.py
@app_commands.context_menu(name="Delete until here")
async def delete(interaction: discord.Interaction, message: discord.Message):
    if not interaction.permissions.manage_messages:
        await interaction.response.send_message("Vous n'avez pas la permission de gérer les messages !",
                                                ephemeral=True)
        return
    if not interaction.app_permissions.manage_messages:
        await interaction.response.send_message("Je n'ai pas la permission de gérer les messages !",
                                                ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True, thinking=True)
    last_id = interaction.channel.last_message_id

    def is_msg(msg):
        if (message.id >> 22) <= (msg.id >> 22) <= (last_id >> 22):
            return msg.id

    del_msg = await message.channel.purge(bulk=True, reason="Admin used bulk delete", check=is_msg)
    await interaction.followup.send(f"{len(del_msg)} messages supprimés !")
