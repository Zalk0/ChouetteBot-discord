import math
from datetime import date

import aiohttp
import discord

from chouette.utils.birthdays import month_to_str
from chouette.utils.hypixel_data import experience_to_level
from chouette.utils.skyblock import get_profile, get_stats, load_skyblock, save_skyblock

SPACES = " " * 38


def format_number(number) -> str:
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
    old_data = await load_skyblock()
    new_data = old_data.copy()
    msg = "Synchro des données de la guilde sur Hypixel Skyblock pour :"
    async with aiohttp.ClientSession() as session:
        for uuid in old_data:
            pseudo = old_data.get(uuid).get("pseudo")
            profile_name = old_data.get(uuid).get("profile")
            profile = await get_profile(session, api_key, uuid, profile_name)
            if not profile[0]:
                raise Exception("Error while updating stats")
            profile = profile[1]
            new_data.get(uuid).update(await get_stats(session, api_key, pseudo, uuid, profile))
            msg += f"\n{SPACES}- {pseudo} sur le profil {profile_name}"
    await save_skyblock(new_data)
    # TODO: handle comparison using old and new data (see issue #56)
    return msg


def parse_data(data: dict) -> tuple[dict, list]:
    """Parse les données de la guilde sur Hypixel Skyblock."""
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
    level_cap = [[], []]

    for player in data:
        for key, value in data[player].items():
            # Handle 'level' and 'networth'
            if key == "level" or key == "networth":
                if key not in ranking:
                    ranking[key] = {}
                ranking[key][data[player]["pseudo"]] = value
            # Handle 'skills'
            if key == "skills":
                for skill in skills:
                    if skill not in ranking:
                        ranking[skill] = {}
                    ranking[skill][data[player]["pseudo"]] = value[skills.index(skill)]
                if "skill average" not in ranking:
                    ranking["skill average"] = {}
                ranking["skill average"][data[player]["pseudo"]] = []
            # Handle 'slayers'
            if key == "slayers":
                for slayer in slayers:
                    if slayer not in ranking:
                        ranking[slayer] = {}
                    ranking[slayer][data[player]["pseudo"]] = value[slayers.index(slayer)]
            if key == "level_cap":
                level_cap[0].append(value[0])
                level_cap[1].append(value[1])

    # Sorting the nested dictionaries by value
    for category in ranking:
        if isinstance(ranking[category], dict):
            unsorted = ranking[category]
            ranking[category] = dict(
                sorted(ranking[category].items(), key=lambda item: item[1], reverse=True)
            )
            # In the case of farming we need to sort the level_cap too
            if category == "farming":
                level_cap[0] = [
                    level_cap[0][list(unsorted.keys()).index(key)] for key in ranking[category]
                ]
            if category == "taming":
                level_cap[1] = [
                    level_cap[1][list(unsorted.keys()).index(key)] for key in ranking[category]
                ]
        else:
            raise ValueError(f"Unknown category while sorting: {category}")
    return ranking, level_cap


def generate_ranking_message(data, category, level_cap):
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
    if category == "skill average":
        skill_average = {}
        for _i, (player, value) in enumerate(data[category].items()):
            skill_average[player] = sum(value) / len(value)
        skill_average = dict(sorted(skill_average.items(), key=lambda item: item[1], reverse=True))

        for i, (player, value) in enumerate(skill_average.items()):
            value = f"{value:.2f}"
            if i == 0:
                message = f"\N{FIRST PLACE MEDAL} **{player}** [{value}]"
            elif i == 1:
                message = f"\N{SECOND PLACE MEDAL} **{player}** [{value}]"
            elif i == 2:
                message = f"\N{THIRD PLACE MEDAL} **{player}** [{value}]"
            else:
                message = f"\N{MEDIUM BLACK CIRCLE} **{player}** [{value}]"
            messages.append(message)
        return data, messages
    for i, (player, value) in enumerate(data[category].items()):
        overflow = None
        if category not in ("level", "networth", "skill average"):
            if category in skills_list:
                if category != "dungeoneering":
                    max_level = 60
                    # Set max level to 50 for skills (alchemy, carpentery, fishing, foraging)
                    if category in ("alchemy", "carpentery", "fishing", "foraging"):
                        max_level = 50
                    # Set max level to level cap for farming
                    if category == "farming":
                        max_level = level_cap[0][i] + 50
                    if category == "taming":
                        max_level = max(min(level_cap[1][i], 60), 50)
                    value, overflow = experience_to_level("skill", value, max_level)
                    data["skill average"][player].append(math.floor(value))
                else:
                    value, overflow = experience_to_level("dungeon", value)
            elif category in slayers_list:
                if category == "zombie":
                    value, overflow = experience_to_level("slayer_zombie", value)
                elif category == "spider":
                    value, overflow = experience_to_level("slayer_spider", value)
                elif category == "vampire":
                    value, overflow = experience_to_level("slayer_vampire", value)
                else:
                    value, overflow = experience_to_level("slayer_web", value)
            else:
                raise ValueError(f"Unknown category in the ranking: {category}")

            if overflow:
                value = f"{value:.0f}"
                overflow = math.floor(overflow)
            else:
                value = f"{value:.2f}"

        elif category == "networth":
            value = format_number(value)

        if i == 0:
            message = f"\N{FIRST PLACE MEDAL} **{player}** [{value}]"
        elif i == 1:
            message = f"\N{SECOND PLACE MEDAL} **{player}** [{value}]"
        elif i == 2:
            message = f"\N{THIRD PLACE MEDAL} **{player}** [{value}]"
        else:
            message = f"\N{MEDIUM BLACK CIRCLE} **{player}** [{value}]"
        if overflow:
            message += f" (*{overflow:,}*)".replace(",", " ")
        messages.append(message)
    return data, messages


async def display_ranking(img: str) -> discord.Embed:
    """Affiche le classement de la guilde sur Hypixel Skyblock."""
    month = await month_to_str(date.today().month)
    year = date.today().year
    ranking = discord.Embed(
        title=f"Classement de début {month} {year}",
        description="Voici le classement de la guilde sur Hypixel Skyblock.\n"
        "Le skill average est sans progression (comme affiché sur Hypixel dans le menu des skills).",
        color=discord.Colour.from_rgb(0, 170, 255),
    )
    ranking.set_footer(text="\N{WHITE HEAVY CHECK MARK} Mis à jour le 1er de chaque mois à 8h00")
    data, level_cap = parse_data(await load_skyblock())
    for category in data:
        if isinstance(data[category], dict):
            data, messages = generate_ranking_message(data, category, level_cap)
            ranking.add_field(
                name=f"**[ {category.capitalize()} ]**",
                value="\n".join(messages),
                inline=False,
            )
    ranking.set_thumbnail(url=img)
    return ranking
