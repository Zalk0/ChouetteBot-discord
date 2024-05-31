from __future__ import annotations

import random
from typing import TYPE_CHECKING

import discord
from discord import app_commands

from chouette.utils.github_api import get_last_update
from chouette.utils.latex_render import latex_render

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot


# Make a LaTeX command
@app_commands.command(name="latex", description="Fait le rendu d'une équation LaTeX")
async def latex(interaction: discord.Interaction[ChouetteBot], equation: str):
    await interaction.response.send_message(file=await latex_render(equation))


# Make the roll command
@app_commands.command(name="roll", description="Lance un dé")
async def die_roll(interaction: discord.Interaction[ChouetteBot]):
    await interaction.response.send_message(f"{random.randint(1, 6)} \N{GAME DIE}")


# Make the ping command
@app_commands.command(name="ping", description="Test la latence du bot")
async def ping(interaction: discord.Interaction[ChouetteBot]):
    await interaction.response.send_message(
        f"Pong ! En {round(interaction.client.latency * 1000)}ms"
    )


# Make a cheh command
@app_commands.command(name="cheh", description="Cheh quelqu'un")
async def cheh(interaction: discord.Interaction[ChouetteBot], user: discord.Member):
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
@app_commands.guild_only
@app_commands.checks.bot_has_permissions(manage_messages=True)
@app_commands.context_menu(
    name="Epingler/Déséingler", description="Épingle ou désépingle un message"
)
async def pin(interaction: discord.Interaction[ChouetteBot], message: discord.Message):
    if message.pinned:
        await message.unpin()
        await interaction.response.send_message("Le message a été désépinglé !", ephemeral=True)
    else:
        await message.pin()
        await interaction.response.send_message("Le message a été épinglé !", ephemeral=True)


# Make a context menu command to delete messages
@app_commands.guild_only
@app_commands.default_permissions(manage_messages=True)
@app_commands.checks.bot_has_permissions(
    manage_messages=True, read_message_history=True, read_messages=True
)
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.context_menu(
    name="Supprime jusqu'ici", description="Supprime les messages jusqu'à celui-ci (inclus)"
)
async def delete(interaction: discord.Interaction[ChouetteBot], message: discord.Message):
    await interaction.response.defer(ephemeral=True, thinking=True)
    last_id = interaction.channel.last_message_id

    def is_msg(msg: discord.Message) -> bool:
        return (message.id >> 22) <= (msg.id >> 22) <= (last_id >> 22)

    del_msg = await message.channel.purge(bulk=True, reason="Admin used bulk delete", check=is_msg)
    await interaction.followup.send(f"{len(del_msg)} messages supprimés !")


# Make a bot information command
@app_commands.command(name="info", description="Affiche les informations du bot")
async def info(interaction: discord.Interaction[ChouetteBot]):
    creators = "Zalko & Gylfirst"
    last_update = await get_last_update()
    github_link = "https://github.com/Zalk0/ChouetteBot-discord"
    dockerhub_link = "https://hub.docker.com/r/gylfirst/chouettebot"
    await interaction.response.send_message(
        f"Bot Discord créé par : {creators}\n\n"
        f"Projet développé pendant notre temps libre. Vous pouvez demander des fonctionnalités sur GitHub.\n"
        f"[Code source](<{github_link}>)\n"
        f"[Image Docker](<{dockerhub_link}>)\n\n"
        f"Dernière mise à jour : {last_update}"
    )
