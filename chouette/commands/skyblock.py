from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

import aiohttp
import discord
from discord import app_commands

from chouette.utils.skyblock_guild import check

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot


# Define command group based on the Group class
class Skyblock(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(name="skyblock", description="Hypixel Skyblock related commands")

    # Make a command to check the version of mods for Hypixel Skyblock
    @app_commands.command(
        name="mods",
        description="Check the latest release of the most popular mods for the Hypixel Skyblock",
    )
    async def mods(self, interaction: discord.Interaction[ChouetteBot]):
        await interaction.response.defer(thinking=True)
        api_github = "https://api.github.com/repos"
        api_modrinth = "https://api.modrinth.com/v2"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{api_github}/Dungeons-Guide/Skyblock-Dungeons-Guide/releases/latest"
            ) as response:
                dungeonsguide = await response.json()
            async with session.get(f"{api_modrinth}/project/GGamhqbw/version") as response:
                notenoughupdates = (await response.json())[0]
            async with session.get(f"{api_modrinth}/project/F35D4vTL/version") as response:
                skyblockaddons = (await response.json())[0]
            async with session.get(f"{api_github}/Skytils/SkytilsMod/releases/latest") as response:
                skytils = await response.json()
        await interaction.followup.send(
            "The latest releases are:\n"
            f"- Dungeons-Guide: `{dungeonsguide['tag_name'].replace('v', '')}` "
            f"[link]({dungeonsguide['assets'][0]['browser_download_url']})\n"
            f"- NotEnoughUpdates: `{notenoughupdates['version_number']}` "
            f"[link]({notenoughupdates['files'][0]['url']})\n"
            f"- SkyblockAddons (forked by Fix3dll): `{skyblockaddons['version_number']}` "
            f"[link]({skyblockaddons['files'][0]['url']})\n"
            f"- Skytils: `{skytils['tag_name'].replace('v', '')}` "
            f"[link]({skytils['assets'][0]['browser_download_url']})"
        )
        
    # Make a command to link the tutorial fHowToSkyblock? from the GitHub repository
    @app_commands.command(
        name="tuto",
        description="Link the tutorial HowToSkyblock? written for beginners",
    )
    async def tuto(self, interaction: discord.Interaction[ChouetteBot]):
        await interaction.response(thinking=True)
        repo_url = "https://github.com/gylfirst/HowToSkyblock"
        await interaction.followup.send(
            f"This tutorial is written for beginners to help them get started with Hypixel Skyblock.\n"
            f"You can find it [here](<{repo_url}>).\n"
            f"Written with :heart: by [gylfirst](<https://github.com/gylfirst>)!"
        )

    # Make a command to check if it's raining in Spider's Den in Hypixel Skyblock
    @app_commands.command(
        name="spider_rain",
        description="Show the time until the next rain and thunderstorm",
    )
    async def spider(self, interaction: discord.Interaction[ChouetteBot]):
        utc_last_thunderstorm = round(
            datetime(2023, 3, 27, 1, 45, 56, tzinfo=timezone.utc).timestamp()
        )
        time_now = round(datetime.now(tz=timezone.utc).timestamp())
        base = time_now - utc_last_thunderstorm
        thunderstorm = base % ((3850 + 1000) * 4)
        rain = thunderstorm % (3850 + 1000)
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

    # Make a command to check if the user is in the guild in-game
    @app_commands.command(name="guild", description="Give a role if in the guild in-game")
    @app_commands.rename(pseudo="pseudo_mc")
    async def in_guild(self, interaction: discord.Interaction[ChouetteBot], pseudo: str):
        if interaction.user.get_role(int(interaction.client.config["HYPIXEL_GUILD_ROLE"])):
            await interaction.response.send_message("Vous avez déjà le rôle !")
            return
        await interaction.response.defer(thinking=True)
        checked = await check(
            pseudo,
            interaction.client.config["HYPIXEL_GUILD_NAME"],
            interaction.user.name,
        )
        if checked is True:
            role = interaction.guild.get_role(int(interaction.client.config["HYPIXEL_GUILD_ROLE"]))
            await interaction.user.add_roles(role)
            await interaction.followup.send("Vous avez été assigné le rôle de membre !")
        else:
            await interaction.followup.send(checked)
