from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

import aiohttp
import discord
from discord import app_commands

from chouette.utils.skyblock import pseudo_to_profile
from chouette.utils.skyblock_guild import check

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot


class Skyblock(app_commands.Group):
    """Classe qui permet de gérer le Skyblock d'Hypixel."""

    def __init__(self) -> None:
        """Initialise la classe Skyblock."""
        super().__init__(name="skyblock", description="Commandes relatives au Skyblock d'Hypixel")

    @app_commands.command(name="mods")
    async def mods(self, interaction: discord.Interaction[ChouetteBot]) -> None:
        """Vérifie les dernières mises à jour des mods populaires du Skyblock d'Hypixel."""
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
        utc_last_thunderstorm = round(
            datetime(2023, 3, 27, 1, 45, 56, tzinfo=timezone.utc).timestamp()
        )
        time_now = round(datetime.now(tz=timezone.utc).timestamp())
        base = time_now - utc_last_thunderstorm
        thunderstorm = base % ((3850 + 1000) * 4)
        rain = thunderstorm % (3850 + 1000)
        if rain <= 3850:
            next_rain = time_now + 3850 - rain
            rain_msg = f"TLa prochaine pluie sera <t:{next_rain}:R>"
        else:
            rain_duration = time_now + 3850 + 1000 - rain
            rain_msg = f"La pluie s'arrêtera <t:{rain_duration}:R>"
        if thunderstorm <= (3850 * 4 + 1000 * 3):
            next_thunderstorm = time_now + (3850 * 4 + 1000 * 3) - thunderstorm
            thunderstorm_msg = f"Le prochain orage sera <t:{next_thunderstorm}:R>"
        else:
            thunderstorm_duration = time_now + (3850 * 4 + 1000 * 4) - thunderstorm
            thunderstorm_msg = f"Le prochain orage s'arrêtera <t:{thunderstorm_duration}:R>"
        await interaction.response.send_message(f"{rain_msg}\n{thunderstorm_msg}")

    @app_commands.command(name="guild")
    @app_commands.rename(pseudo="pseudo_mc")
    async def in_guild(self, interaction: discord.Interaction[ChouetteBot], pseudo: str) -> None:
        """Donne un rôle sur le Discord si le joueur est dans la guilde."""
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

    @app_commands.command(name="link")
    @app_commands.rename(pseudo="pseudo_mc")
    @app_commands.describe(pseudo="Ton pseudo Minecraft", profile="Ton profil Skyblock préféré")
    async def link(
        self, interaction: discord.Interaction[ChouetteBot], pseudo: str, profile: str | None
    ):
        """Lie le profil Hypixel Skyblock du joueur."""
        await interaction.response.defer(ephemeral=True, thinking=True)
        discord_pseudo = interaction.user.name
        async with aiohttp.ClientSession() as session:
            profile_name = await pseudo_to_profile(
                session, interaction.client.config["HYPIXEL_KEY"], discord_pseudo, pseudo, profile
            )
        if isinstance(profile_name, str):
            interaction.client.bot_logger.error(profile_name)
            await interaction.followup.send(f"Il y a eu une erreur :\n`{profile_name}`")
            return
        await interaction.followup.send(
            f"Vous êtes bien connecté et le profil "
            f"{profile_name.get('profile')} a été enregistré."
        )
