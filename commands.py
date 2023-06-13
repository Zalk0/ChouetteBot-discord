import random
from datetime import datetime

import discord
import requests

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
    @tree.context_menu(name="Delete until here")
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

    # Make a LaTeX command
    @tree.command(name="latex", description="Renders LaTeX equation")
    async def latex(interaction: discord.Interaction, equation: str):
        await interaction.response.send_message(file=await latex_render(equation))

    # Make a command to check the version of mods for Hypixel Skyblock
    @tree.command(name="mods_skyblock",
                  description="Checks the latest release of some of the most popular mods for the Hypixel Skyblock")
    async def skyblock(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        api_github = "https://api.github.com/repos/"
        dungeonsguide = requests.get(f"{api_github}Dungeons-Guide/Skyblock-Dungeons-Guide/releases/latest").json()
        notenoughupdates = requests.get(f"{api_github}Moulberry/NotEnoughUpdates/releases/latest").json()
        skyblockaddons = requests.get(f"{api_github}BiscuitDevelopment/SkyblockAddons/releases/latest").json()
        skytils = requests.get(f"{api_github}Skytils/SkytilsMod/releases/latest").json()
        await interaction.followup.send(f"The latest releases are :\n"
                                        f"Dungeons Guide : `{dungeonsguide['name'].replace('v', '')}`\n"
                                        f"Not Enough Updates : `{notenoughupdates['name']}`\n"
                                        f"SkyblockAddons : `{skyblockaddons['name'].replace('Patch v', '')}`\n"
                                        f"Skytils : `{skytils['name'].replace('Skytils ', '')}`")

    # Make a command to check if it's raining in Spider's Den in Hypixel Skyblock
    @tree.command(name="spider_rain", description="Shows time until next rain and thunderstorm")
    async def spider(interaction: discord.Interaction):
        utc_last_thunderstorm = datetime(2023, 3, 27, 1, 45, 56).timestamp()
        base = round(datetime.utcnow().timestamp() - utc_last_thunderstorm)
        thunderstorm = base % ((3850 + 1000) * 4)
        rain = thunderstorm % (3850 + 1000)
        time_now = round(datetime.now().timestamp())
        if rain <= 3850:
            next_rain = time_now + 3850 - rain
            rain_msg = f"The next rain will be <t:{next_rain}:R>"
        else:
            rain_duration = time_now + 3850 + 1000 - rain
            rain_msg = f"The rain will end <t:{rain_duration}:R>"
        if thunderstorm <= (3850 * 4 + 1000 * 3):
            next_thunderstorm = time_now + (3850 * 4 + 1000 * 3) - thunderstorm
            thunderstorm_msg = f"The next thunderstorm will be <t:{next_thunderstorm}:R>"
        else:
            thunderstorm_duration = time_now + (3850 * 4 + 1000 * 4) - thunderstorm
            thunderstorm_msg = f"The thunderstorm will end <t:{thunderstorm_duration}:R>"
        await interaction.response.send_message(f"{rain_msg}\n{thunderstorm_msg}")
