import math
from datetime import date

import aiohttp
import discord

from chouette.utils.birthdays import month_to_str
from chouette.utils.hypixel_data import experience_to_level
from chouette.utils.skyblock import (
    get_hypixel_player,
    get_profile,
    get_stats,
    load_skyblock,
    save_skyblock,
)

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


def format_ranking_message(player: str, value: str, i: int) -> str:
    """Formate le message pour les données du classement de la guilde sur Hypixel Skyblock."""
    if i == 0:
        message = f"\N{FIRST PLACE MEDAL} **{player}** [{value}]"
    elif i == 1:
        message = f"\N{SECOND PLACE MEDAL} **{player}** [{value}]"
    elif i == 2:
        message = f"\N{THIRD PLACE MEDAL} **{player}** [{value}]"
    else:
        message = f"\N{MEDIUM BLACK CIRCLE} **{player}** [{value}]"
    return message


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
            player = await get_hypixel_player(session, api_key, uuid)
            new_data.get(uuid).update(await get_stats(session, pseudo, uuid, player, profile))
            msg += f"\n{SPACES}- {pseudo} sur le profil {profile_name}"
    await save_skyblock(new_data)
    # TODO: handle comparison using old and new data (see issue #56)
    return msg


def parse_data(data: dict) -> dict:
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
        "carpentry",
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
                        ranking[skill] = {"level": {}, "overflow": {}}
                if "skill average" not in ranking:
                    ranking["skill average"] = {}
                ranking["skill average"][data[player]["pseudo"]] = []
            # Handle 'slayers'
            if key == "slayers":
                for slayer in slayers:
                    if slayer not in ranking:
                        ranking[slayer] = {"level": {}, "overflow": {}}
            if key == "level_cap":
                level_cap[0].append(value[0])
                level_cap[1].append(value[1])

    # Calculate the level and overflow for each skill for each player
    for player_index, player in enumerate(data):
        for skill in skills:
            if skill != "dungeoneering":
                if skill == "farming":
                    level, overflow = experience_to_level(
                        "skill",
                        data[player]["skills"][skills.index(skill)],
                        level_cap[0][player_index] + 50,
                    )
                elif skill == "taming":
                    level, overflow = experience_to_level(
                        "skill",
                        data[player]["skills"][skills.index(skill)],
                        level_cap[1][player_index] if level_cap[1][player_index] > 50 else 50,
                    )
                else:
                    if skill in ["fishing", "alchemy", "carpentry", "foraging"]:
                        level, overflow = experience_to_level(
                            "skill", data[player]["skills"][skills.index(skill)], max_level=50
                        )
                    else:
                        level, overflow = experience_to_level(
                            "skill", data[player]["skills"][skills.index(skill)]
                        )
            else:
                level, overflow = experience_to_level(
                    "dungeon", data[player]["skills"][skills.index(skill)], 50
                )
            ranking[skill]["level"][data[player]["pseudo"]] = level
            ranking[skill]["overflow"][data[player]["pseudo"]] = overflow
        # Calculate the level and overflow for each slayer for each player
        for slayer in slayers:
            level, overflow = experience_to_level(
                f"slayer_{slayer}",
                data[player]["slayers"][slayers.index(slayer)],
            )
            ranking[slayer]["level"][data[player]["pseudo"]] = level
            ranking[slayer]["overflow"][data[player]["pseudo"]] = overflow

    # Sorting the nested dictionaries by value
    sorted_ranking: dict = ranking.copy()
    for category in ranking:
        if isinstance(ranking[category], dict):
            # Level and Networth
            if category in ["level", "networth"]:
                sorted_ranking[category] = dict(
                    sorted(ranking[category].items(), key=lambda item: item[1], reverse=True)
                )
            # Skills
            if category in skills:
                sorted_ranking[category] = {
                    "level": dict(
                        sorted(
                            ranking[category]["level"].items(),
                            key=lambda item: (item[1], ranking[category]["overflow"][item[0]]),
                            reverse=True,
                        )
                    ),
                    "overflow": dict(ranking[category]["overflow"].items()),
                }
            # Slayers
            if category in slayers:
                sorted_ranking[category] = {
                    "level": dict(
                        sorted(
                            ranking[category]["level"].items(),
                            key=lambda item: (item[1], ranking[category]["overflow"][item[0]]),
                            reverse=True,
                        )
                    ),
                    "overflow": dict(ranking[category]["overflow"].items()),
                }
        else:
            raise ValueError(f"Unknown category while sorting the ranking: {category}")
    return sorted_ranking


def generate_ranking_message(data, category) -> list[str]:
    skills_list: list[str] = [
        "fishing",
        "alchemy",
        "mining",
        "farming",
        "enchanting",
        "taming",
        "foraging",
        "carpentry",
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
    messages: list = []
    # Level
    if category == "level":
        for i, (player, value) in enumerate(data[category].items()):
            value = f"{value:.2f}"
            message = format_ranking_message(player, value, i)
            messages.append(message)
    # Networth
    if category == "networth":
        for i, (player, value) in enumerate(data[category].items()):
            value = format_number(value)
            message = format_ranking_message(player, value, i)
            messages.append(message)
    # Skills
    if category in skills_list:
        for i, (player, value) in enumerate(data[category]["level"].items()):
            overflow = data[category]["overflow"][player]
            if overflow:
                value = f"{value:.0f}"
                overflow = math.floor(overflow)
            else:
                value = f"{value:.2f}"
            message = format_ranking_message(player, value, i)
            if overflow:
                message += f" (*{overflow:,}*)".replace(",", " ")
            messages.append(message)
    # Skill average
    skills_avg: list[str] = skills_list.copy()
    skills_avg.remove("dungeoneering")
    if category == "skill average":
        for player in data[category]:
            total = []
            # Calculate the average of the skills
            for skill in skills_avg:
                total.append(math.floor(data[skill]["level"][player]))
            average = math.fsum(total) / len(total)
            data[category][player] = average
        # Sort the skill average
        data[category] = dict(
            sorted(data[category].items(), key=lambda item: item[1], reverse=True)
        )
        for i, (player, value) in enumerate(data[category].items()):
            value = f"{value:.2f}"
            message = format_ranking_message(player, value, i)
            messages.append(message)
    # Slayers
    if category in slayers_list:
        for i, (player, value) in enumerate(data[category]["level"].items()):
            overflow = data[category]["overflow"][player]
            if overflow:
                value = f"{value:.0f}"
                overflow = math.floor(overflow)
            else:
                value = f"{value:.2f}"
            message = format_ranking_message(player, value, i)
            if overflow:
                message += f" (*{overflow:,}*)".replace(",", " ")
            messages.append(message)
    return messages


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
    data = parse_data(await load_skyblock())
    for category in data:
        if isinstance(data[category], dict):
            messages = generate_ranking_message(data, category)
            ranking.add_field(
                name=f"**[ {category.capitalize()} ]**",
                value="\n".join(messages),
                inline=False,
            )
    ranking.set_thumbnail(url=img)
    return ranking
