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
            new_data.get(uuid).update(await get_stats(session, pseudo, uuid, profile))
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
            # Handle 'slayers'
            if key == "slayers":
                for slayer in slayers:
                    if slayer not in ranking:
                        ranking[slayer] = {}
                    ranking[slayer][data[player]["pseudo"]] = value[slayers.index(slayer)]
            if key == "level_cap":
                level_cap[0].append(value[0])
                # TODO: for taming
                # -> level_cap[1].append(value[1])

    # Sorting the nested dictionaries by value
    for category in ranking:
        if isinstance(ranking[category], dict):
            unsorted = ranking[category]
            ranking[category] = dict(
                sorted(ranking[category].items(), key=lambda item: item[1], reverse=True)
            )
            # In the case of farming we need sort the level_cap too
            if category == "farming":
                level_cap[0] = [
                    level_cap[0][list(unsorted.keys()).index(key)] for key in ranking[category]
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
    for i, (player, value) in enumerate(data[category].items()):
        if category != "level" and category != "networth":
            if category in skills_list:
                if category != "dungeoneering":
                    value = experience_to_level(type_xp="skill", xp_amount=value)
                else:
                    value = experience_to_level(type_xp="dungeon", xp_amount=value)
                # Set max level to 50 for skills (alchemy, carpentery, fishing, foraging)
                if category in ("alchemy", "carpentery", "fishing", "foraging", "taming"):
                    value = min(value, 50.00)
                # Set max level to level cap for farming
                if category == "farming":
                    value = min(value, level_cap[0][i] + 50)
                    # TODO: if taming -> level_cap[1][i] + 50
            elif category in slayers_list:
                if category == "zombie":
                    value = experience_to_level(type_xp="slayer_zombie", xp_amount=value)
                elif category == "spider":
                    value = experience_to_level(type_xp="slayer_spider", xp_amount=value)
                elif category == "vampire":
                    value = experience_to_level(type_xp="slayer_vampire", xp_amount=value)
                else:
                    value = experience_to_level(type_xp="slayer_web", xp_amount=value)
            else:
                raise ValueError(f"Unknown category in the ranking: {category}")
            value = f"{value:.2f}"
        elif category == "networth":
            value = format_number(value)

        if i == 0:
            message = f"\N{FIRST PLACE MEDAL} **{player}** ({value})"
        elif i == 1:
            message = f"\N{SECOND PLACE MEDAL} **{player}** ({value})"
        elif i == 2:
            message = f"\N{THIRD PLACE MEDAL} **{player}** ({value})"
        else:
            message = f"\N{MEDIUM BLACK CIRCLE} **{player}** ({value})"
        messages.append(message)
    return messages


async def display_ranking(img: str) -> discord.Embed:
    """Affiche le classement de la guilde sur Hypixel Skyblock."""
    month = await month_to_str(date.today().month)
    year = date.today().year
    ranking = discord.Embed(
        title=f"Classement de début {month} {year}",
        description="Voici le classement de la guilde sur Hypixel Skyblock.",
        color=discord.Colour.from_rgb(0, 170, 255),
    )
    ranking.set_footer(text="\N{WHITE HEAVY CHECK MARK} Mis à jour le 1er de chaque mois à 8h00")
    data, level_cap = parse_data(await load_skyblock())
    for category in data:
        if isinstance(data[category], dict):
            messages = generate_ranking_message(data, category, level_cap)
            ranking.add_field(
                name=f"**[ {category.capitalize()} ]**",
                value="\n".join(messages),
                inline=False,
            )
    ranking.set_thumbnail(url=img)
    return ranking
