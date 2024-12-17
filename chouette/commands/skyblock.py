from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

import aiohttp
import discord
from discord import app_commands

from chouette.utils.skyblock import pseudo_to_profile

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot


class Skyblock(app_commands.Group):
    """Classe qui permet de gérer le Skyblock d'Hypixel."""

    def __init__(self) -> None:
        """Initialise la classe Skyblock."""
        super().__init__(name="skyblock", description="Commandes relatives au Skyblock d'Hypixel")

    @app_commands.command(
        name="mods",
        description="Vérifie les dernières mises à jour des mods selon la version de Minecraft",
    )
    @app_commands.rename(mc_version="version")
    @app_commands.describe(mc_version="Ta version de Minecraft")
    @app_commands.choices(
        mc_version=[
            app_commands.Choice(name="1.8.9", value="1.8.9"),
            app_commands.Choice(name="1.21.1", value="1.21.1"),
        ]
    )
    async def mods(
        self, interaction: discord.Interaction[ChouetteBot], mc_version: app_commands.Choice[str]
    ) -> None:
        """Vérifie les dernières mises à jour des mods populaires du Skyblock d'Hypixel."""
        await interaction.response.defer(thinking=True)
        api_github = "https://api.github.com/repos"
        api_modrinth = "https://api.modrinth.com/v2"
        if mc_version.value == "1.8.9":
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{api_github}/Dungeons-Guide/Skyblock-Dungeons-Guide/releases/latest"
                ) as response:
                    dungeonsguide = await response.json()
                async with session.get(f"{api_modrinth}/project/GGamhqbw/version") as response:
                    notenoughupdates = (await response.json())[0]
                async with session.get(f"{api_modrinth}/project/F35D4vTL/version") as response:
                    skyblockaddons = (await response.json())[0]
                async with session.get(
                    f"{api_github}/Skytils/SkytilsMod/releases/latest"
                ) as response:
                    skytils = await response.json()
            message = (
                f"Version de Minecraft: `{mc_version.value}`\n"
                f"--------------------------------\n"
                "Les dernières mises à jour sont :\n"
                f"- Dungeons-Guide: `{dungeonsguide['tag_name'].replace('v', '')}` "
                f"[lien]({dungeonsguide['assets'][0]['browser_download_url']})\n"
                f"- NotEnoughUpdates: `{notenoughupdates['version_number']}` "
                f"[lien]({notenoughupdates['files'][0]['url']})\n"
                f"- SkyblockAddons (forked by Fix3dll): `{skyblockaddons['version_number']}` "
                f"[lien]({skyblockaddons['files'][0]['url']})\n"
                f"- Skytils: `{skytils['tag_name'].replace('v', '')}` "
                f"[lien]({skytils['assets'][0]['browser_download_url']})"
            )

        # `else` possible car seulement 2 versions de Minecraft
        elif mc_version.value == "1.21.1":
            # Mod loader: Fabric
            # Some mods are only available for Fabric, but they can have other loaders in the future
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{api_modrinth}/project/axe0DxiW/version") as response:
                    aaron = await response.json()
                    for entry in aaron:
                        if "1.21.1" in entry.get("game_versions", []) and "fabric" in entry.get(
                            "loaders", []
                        ):
                            aaron = entry
                            break
                async with session.get(f"{api_modrinth}/project/IJNUBZ2a/version") as response:
                    firmament = await response.json()
                    for entry in firmament:
                        if "1.21.1" in entry.get("game_versions", []) and "fabric" in entry.get(
                            "loaders", []
                        ):
                            firmament = entry
                            break
                async with session.get(f"{api_modrinth}/project/nfn13YXA/version") as response:
                    roughly_enough_items = await response.json()
                    for entry in roughly_enough_items:
                        if "1.21.1" in entry.get("game_versions", []) and "fabric" in entry.get(
                            "loaders", []
                        ):
                            roughly_enough_items = entry
                            break
                async with session.get(f"{api_modrinth}/project/y6DuFGwJ/version") as response:
                    skyblocker = await response.json()
                    for entry in skyblocker:
                        if "1.21.1" in entry.get("game_versions", []) and "fabric" in entry.get(
                            "loaders", []
                        ):
                            skyblocker = entry
                            break
            message = (
                f"Version de Minecraft: `{mc_version.value}`\n"
                f"Mod loader: `Fabric`\n"
                "--------------------------------\n"
                "Les dernières mises à jour sont :\n"
                f"- Aaron's Mod: `{aaron['version_number'].split('+')[0]}` "
                f"[lien]({aaron['files'][0]['url']})\n"
                f"- Firmament: `{firmament['version_number'].split('+')[0]}` "
                f"[lien]({firmament['files'][0]['url']})\n"
                f"- Roughly Enough Items (REI): `{roughly_enough_items['version_number'].split('+')[0]}` "
                f"[lien]({roughly_enough_items['files'][0]['url']})\n"
                f"- Skyblocker: `{skyblocker['version_number'].split('+')[0].replace('v', '')}` "
                f"[lien]({skyblocker['files'][0]['url']})\n"
            )
        await interaction.followup.send(message)

    @app_commands.command(name="tuto")
    async def tuto(self, interaction: discord.Interaction[ChouetteBot]) -> None:
        """Donne le lien du tutoriel pour débuter sur le Skyblock d'Hypixel."""
        repo_url = "https://github.com/gylfirst/HowToSkyblock"
        strip_color = discord.Colour.from_str(value="#DAA520")  # HTML name: GoldenRod
        embed_tuto = discord.Embed(
            title="Tutoriel pour débuter sur le Skyblock d'Hypixel",
            description="Ce tutoriel est écrit pour que les débutants puissent jouer au Skyblock d'Hypixel facilement.",
            color=strip_color,
        )
        embed_tuto.set_author(name="Gylfirst", url="https://github.com/gylfirst")
        embed_tuto.set_thumbnail(url="https://hypixel.net/attachments/1608783256403-png.2210524")
        embed_tuto.add_field(
            name="Comment utiliser le tutoriel ?",
            value=f"Il suffit de cliquer sur le lien ci-dessous pour accéder au tutoriel.\n{repo_url}",
            inline=False,
        )
        embed_tuto.set_footer(text="HowToSkyblock")
        await interaction.response.send_message(embed=embed_tuto)

    @app_commands.command(name="spider_rain")
    async def spider(self, interaction: discord.Interaction[ChouetteBot]) -> None:
        """Indique le temps de la prochaine pluie ou orage sur Spider's Den."""
        # The weather cycle for spider den starts at the start of the skyblock (timestamp 1560275700) and repeats
        time_now = round(datetime.now(tz=timezone.utc).timestamp())
        skyblock_age = time_now - 1560275700

        # variables for cooldown, duration and interval for thunderstorm and rain
        # Sunny -> Thunderstorm -> Sunny -> Rain -> Sunny -> Rain
        # Sunny: 2400secs
        # Rain and Thunderstorm: 1200secs
        cooldown = 2400
        duration = 1200
        thunderstorm_interval = 3

        thunderstorm = skyblock_age % ((cooldown + duration) * thunderstorm_interval)
        rain = skyblock_age % (cooldown + duration)

        # rain
        if cooldown <= rain:
            time_left = (cooldown + duration) - rain
            rain_duration = time_now + time_left
            rain_msg = f"La pluie s'arrêtera <t:{rain_duration}:R>"
        else:
            next_rain = time_now + cooldown - rain
            rain_msg = f"La prochaine pluie sera <t:{next_rain}:R>"

        # thunderstorm
        if (cooldown <= thunderstorm) and (thunderstorm < (cooldown + duration)):
            time_left = (cooldown + duration) - rain
            thunderstorm_duration = time_now + time_left
            thunderstorm_msg = f"Le prochain orage s'arrêtera <t:{thunderstorm_duration}:R>"
        else:
            if thunderstorm < cooldown:
                next_thunderstorm = time_now + cooldown - thunderstorm
            elif (cooldown + duration) <= thunderstorm:
                next_thunderstorm = (
                    time_now + (cooldown + duration) * (thunderstorm_interval) + cooldown
                ) - thunderstorm
            thunderstorm_msg = f"Le prochain orage sera <t:{next_thunderstorm}:R>"

        await interaction.response.send_message(f"{rain_msg}\n{thunderstorm_msg}")

    @app_commands.command(name="link")
    @app_commands.rename(pseudo="pseudo_mc")
    @app_commands.describe(pseudo="Ton pseudo Minecraft", profile="Ton profil Skyblock préféré")
    # Cooldown 1 use per 60 seconds
    @app_commands.checks.cooldown(rate=1, per=60)
    async def link(
        self, interaction: discord.Interaction[ChouetteBot], pseudo: str, profile: str | None
    ):
        """Lie le profil Hypixel Skyblock du joueur."""
        await interaction.response.defer(thinking=True)
        discord_pseudo = interaction.user.name
        async with aiohttp.ClientSession() as session:
            profile_name = await pseudo_to_profile(
                session, interaction.client, discord_pseudo, pseudo, profile
            )
        if isinstance(profile_name, str):
            interaction.client.bot_logger.error(profile_name)
            await interaction.followup.send(f"Il y a eu une erreur :\n`{profile_name}`")
            return
        await interaction.followup.send(
            f"Vous êtes bien connecté et le profil "
            f"{profile_name.get('profile')} a été enregistré."
        )
