from datetime import date
from pathlib import Path

import aiohttp
import discord

from chouette.utils.birthdays import month_to_str
from chouette.utils.data_io import data_read, data_write
from chouette.utils.hypixel_data import experience_to_level
from chouette.utils.skyblock import pseudo_to_profile

SKYBLOCK_FILE: Path = Path("data", "skyblock.toml")
RANKING_FILE: Path = Path("data", "ranking.toml")
SPACES = " " * 38


async def format_number(number) -> str:
    """Permet de formater un nombre en K, M ou B."""
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f}B"
    if number >= 1_000_000:
        return f"{number / 1_000_000:.0f}M"
    if number >= 1_000:
        return f"{number / 1_000:.0f}K"
    return str(number)


async def update_stats(api_key: str) -> str:
    """Crée le classement de la guilde sur Hypixel Skyblock."""
    data = await data_read(SKYBLOCK_FILE)
    msg = "Synchro des données de la guilde sur Hypixel Skyblock pour :"
    async with aiohttp.ClientSession() as session:
        for player in data:
            result = await pseudo_to_profile(
                session,
                api_key,
                data[player]["discord"],
                data[player]["pseudo"],
                data[player]["profile"],
            )
            msg += f"\n{SPACES}- {result.get('pseudo')} sur le profil {result.get('profile')}"
    return msg


async def parse_data() -> dict:
    """Parse les données de la guilde sur Hypixel Skyblock."""
    data = await data_read(SKYBLOCK_FILE)
    ranking = {}
    skills = [
        "fishing",
        "alchemy",
        "mining",
        "farming",
        "enchanting",
        "taming",
        "foraging",
        "carpentery",
        "combat",
        "dungeoneering",
    ]
    slayers = ["zombie", "spider", "wolf", "enderman", "blaze", "vampire"]
    level_cap = []

    for player in data:
        for key, value in data[player].items():
            # Handle 'level' and 'networth'
            if key == "level" or key == "networth":
                if key not in ranking:
                    ranking[key] = {}
                ranking[key][data[player]["pseudo"]] = value
            # Handle 'skills'
            elif key == "skills":
                for skill in skills:
                    if skill not in ranking:
                        ranking[skill] = {}
                    ranking[skill][data[player]["pseudo"]] = value[skills.index(skill)]
            # Handle 'slayers'
            elif key == "slayers":
                for slayer in slayers:
                    if slayer not in ranking:
                        ranking[slayer] = {}
                    ranking[slayer][data[player]["pseudo"]] = value[slayers.index(slayer)]
            elif key == "level_cap":
                level_cap.append(value[0])
                # TODO: for taming
                # -> level_cap.append(value[1])
            # Skip other keys
            else:
                continue

    # Sorting the nested dictionaries by value
    for category in ranking:
        if isinstance(ranking[category], dict):
            ranking[category] = dict(
                sorted(ranking[category].items(), key=lambda item: item[1], reverse=True)
            )
        elif category == "skills" or category == "slayers":
            for subcategory in ranking[category]:
                ranking[category][subcategory] = dict(
                    sorted(
                        ranking[category][subcategory].items(),
                        key=lambda item: item[1],
                        reverse=True,
                    )
                )
    await data_write(ranking, RANKING_FILE)
    return ranking, level_cap


async def generate_ranking_message(data, category, level_cap):
    skills_list: list[str] = [
        "fishing",
        "alchemy",
        "mining",
        "farming",
        "enchanting",
        "taming",
        "foraging",
        "carpentery",
        "combat",
        "dungeoneering",
    ]
    slayers_list: list[str] = [
        "zombie",
        "spider",
        "wolf",
        "enderman",
        "blaze",
        "vampire",
    ]
    messages = []
    for i, (player, value) in enumerate(data[category].items()):
        if category != "level" and category != "networth":
            if category in skills_list:
                if category != "dungeoneering":
                    value = await experience_to_level(type_xp="skill", xp_amount=value)
                else:
                    value = await experience_to_level(type_xp="dungeon", xp_amount=value)
                # set max level to 50 for skills (alchemy, carpentery, fishing, foraging)
                if (
                    category == "alchemy"
                    or category == "carpentery"
                    or category == "fishing"
                    or category == "foraging"
                ):
                    value = min(value, 50.00)
                # set max level to 50 for farming with level cap
                if category == "farming":
                    value = min(value, level_cap[0] + 50)
                # set max level to 50 for taming with level cap
                # TODO: if taming -> level_cap[1] + 50
            elif category in slayers_list:
                if category == "zombie":
                    value = await experience_to_level(type_xp="slayer_zombie", xp_amount=value)
                elif category == "spider":
                    value = await experience_to_level(type_xp="slayer_spider", xp_amount=value)
                elif category == "vampire":
                    value = await experience_to_level(type_xp="slayer_vampire", xp_amount=value)
                else:
                    value = await experience_to_level(type_xp="slayer_web", xp_amount=value)
            else:
                raise ValueError(f"Unknown category: {category}")
            value = f"{value:.2f}"
        elif category == "networth":
            value = await format_number(value)
        if i == 0:
            message = f"🥇 **{player}** ({value})"
        elif i == 1:
            message = f"🥈 **{player}** ({value})"
        elif i == 2:
            message = f"🥉 **{player}** ({value})"
        else:
            message = f"⚫ **{player}** ({value})"
        messages.append(message)
    return messages


async def display_ranking(img: str) -> discord.Embed:
    """Affiche le classement de la guilde sur Hypixel Skyblock."""
    mois = await month_to_str(date.today().month)
    annee = date.today().year
    ranking = discord.Embed(
        title=f"Classement du mois de {mois} {annee}",
        description="Voici le classement de la guilde sur Hypixel Skyblock.",
        color=discord.Colour.from_rgb(0, 170, 255),
    )
    ranking.set_footer(text="✅ Mis à jour le 1er de chaque mois à 8h00")
    data, level_cap = await parse_data()
    for category in data:
        if isinstance(data[category], dict):
            messages = await generate_ranking_message(data, category, level_cap)
            ranking.add_field(
                name=f"**[ {category.capitalize()} ]**",
                value="\n".join(messages),
                inline=False,
            )
    ranking.set_thumbnail(url=img)
    return ranking
