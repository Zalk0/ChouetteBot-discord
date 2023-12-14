from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import aiohttp
import discord
from discord import app_commands

from utils.skyblock_guild import check

if TYPE_CHECKING:
    from bot import ChouetteBot


# Define command group based on the Group class
class Skyblock(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(
            name="skyblock", description="Hypixel Skyblock related commands"
        )

    # Make a command to check the version of mods for Hypixel Skyblock
    @app_commands.command(
        name="mods",
        description="Check the latest release of the most popular mods for the Hypixel Skyblock",
    )
    async def mods(self, interaction: discord.Interaction[ChouetteBot]):
        await interaction.response.defer(thinking=True)
        api_github = "https://api.github.com/repos/"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{api_github}Dungeons-Guide/Skyblock-Dungeons-Guide/releases/latest"
            ) as response:
                dungeonsguide = await response.json()
            async with session.get(
                f"{api_github}NotEnoughUpdates/NotEnoughUpdates/releases"
            ) as response:
                notenoughupdates = await response.json()
            async with session.get(
                f"{api_github}Fix3dll/SkyblockAddons/contents/gradle.properties",
                headers={"Accept": "application/vnd.github.raw"},
            ) as response:
                content = await response.text()
                sba_version = re.search(
                    r"^version\s?=\s?(.*)$", content, re.MULTILINE
                )
            async with session.get(
                f"{api_github}Fix3dll/SkyblockAddons/actions/runs"
            ) as response:
                content = await response.json()
                for run in content["workflow_runs"]:
                    if run["head_branch"] == "main" && run["conclusion"] == "success":
                        skyblockaddons = (
                            f"{sba_version.group(1)}+{run['run_number']}"
                        )
                        break
            async with session.get(
                f"{api_github}Skytils/SkytilsMod/releases/latest"
            ) as response:
                skytils = await response.json()
        await interaction.followup.send(
            f"The latest releases are:\n"
            f"- Dungeons-Guide: `{dungeonsguide['tag_name']}` "
            f"[link]({dungeonsguide['assets'][0]['browser_download_url']})\n"
            f"- NotEnoughUpdates: `{notenoughupdates[0]['tag_name'].replace('v', '')}` "
            f"[link]({notenoughupdates[0]['assets'][0]['browser_download_url']})\n"
            f"- SkyblockAddons (forked by Fix3dll): `{skyblockaddons}` "
            f"[link](https://nightly.link/Fix3dll/SkyblockAddons/workflows/build/main/build_artifacts.zip)\n"
            f"- Skytils: `{skytils['tag_name'].replace('v', '')}` "
            f"[link]({skytils['assets'][0]['browser_download_url']})"
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
            thunderstorm_msg = (
                f"The next thunderstorm will be <t:{next_thunderstorm}:R>"
            )
        else:
            thunderstorm_duration = (
                time_now + (3850 * 4 + 1000 * 4) - thunderstorm
            )
            thunderstorm_msg = (
                f"The thunderstorm will end <t:{thunderstorm_duration}:R>"
            )
        await interaction.response.send_message(
            f"{rain_msg}\n{thunderstorm_msg}"
        )

    # Make a command to check if the user is in the guild in-game
    @app_commands.command(
        name="guild", description="Give a role if in the guild in-game"
    )
    @app_commands.rename(pseudo="pseudo_mc")
    async def in_guild(
        self, interaction: discord.Interaction[ChouetteBot], pseudo: str
    ):
        if interaction.user.get_role(
            int(interaction.client.config["HYPIXEL_GUILD_ROLE"])
        ):
            await interaction.response.send_message("Vous avez déjà le rôle !")
            return
        await interaction.response.defer(thinking=True)
        checked = check(
            pseudo,
            interaction.client.config["HYPIXEL_GUILD_NAME"],
            interaction.user.global_name,
        )
        if checked:
            role = interaction.guild.get_role(
                int(interaction.client.config["HYPIXEL_GUILD_ROLE"])
            )
            await interaction.user.add_roles(role)
            await interaction.followup.send(
                "Vous avez été assigné le rôle de membre !"
            )
        else:
            await interaction.followup.send(checked)
