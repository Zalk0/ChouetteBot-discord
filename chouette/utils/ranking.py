import copy
import math
from datetime import date
from itertools import chain

import discord
from aiohttp import ClientSession

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
    """Formate un nombre en K, M ou B.

    Args:
        number (int): Le nombre à formater.

    Returns:
        str: Le nombre formaté.
    """
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f}B"
    if number >= 1_000_000:
        return f"{number / 1_000_000:.0f}M"
    if number >= 1_000:
        return f"{number / 1_000:.0f}K"
    return str(number)


def format_ranking_message(player: str, value: str, index: int, position: int) -> str:
    """Formate le message pour les données du classement de la guilde sur Hypixel Skyblock.

    Args:
        player (str): Le pseudo du joueur.
        value (str): La valeur à afficher (niveau, networth, etc.).
        index (int): L'index du joueur dans le classement.
        position (int): -1 si le joueur a descendu, 0 s'il n'a pas bougé, 1 s'il a monté.

    Returns:
        str: Le message formaté.
    """
    # Codes emoji custom pour les positions (discord developer portal app)
    if position == 1:
        # emoji custom 'green_up_arrow'
        message = "<:gua:1319980544674762753> "
    elif position == -1:
        # emoji custom 'red_down_arrow'
        message = "<:rda:1319980559581057045> "
    else:
        message = "\U0001f536 "
    if index == 0:
        message += f"\N{FIRST PLACE MEDAL} **{player}** [{value}]"
    elif index == 1:
        message += f"\N{SECOND PLACE MEDAL} **{player}** [{value}]"
    elif index == 2:
        message += f"\N{THIRD PLACE MEDAL} **{player}** [{value}]"
    else:
        message += f"\N{MEDIUM BLACK CIRCLE} **{player}** [{value}]"
    return message


async def update_stats(session: ClientSession, api_key: str) -> tuple[str, dict]:
    """Met à jour les statistiques de la guilde sur Hypixel Skyblock.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        api_key (str): La clé API d'Hypixel pour accéder aux données.

    Raises:
        Exception: Si une erreur survient lors de la mise à jour des statistiques.

    Returns:
        tuple[str, dict]: Le message de mise à jour et les anciennes données.
    """
    old_data = await load_skyblock()
    new_data = copy.deepcopy(old_data)
    msg = "Synchro des données de la guilde sur Hypixel Skyblock pour :"
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
    old_data = parse_data(old_data)
    return msg, old_data


def parse_data(data: dict) -> dict:
    """Parse les données de la guilde sur Hypixel Skyblock.

    Args:
        data (dict): Les données à parser.

    Raises:
        ValueError: Si une catégorie inconnue est rencontrée lors du tri des données.

    Returns:
        dict: Les données parsées.
    """
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
            # Gère 'level' et 'networth'
            if key == "level" or key == "networth":
                if key not in ranking:
                    ranking[key] = {}
                ranking[key][data[player]["pseudo"]] = value
            # Gère 'skills'
            if key == "skills":
                for skill in skills:
                    if skill not in ranking:
                        ranking[skill] = {"level": {}, "overflow": {}}
                if "skill average" not in ranking:
                    ranking["skill average"] = {}
                ranking["skill average"][data[player]["pseudo"]] = None
            # Gère 'slayers'
            if key == "slayers":
                for slayer in slayers:
                    if slayer not in ranking:
                        ranking[slayer] = {"level": {}, "overflow": {}}
            # Gère les 'level_cap'
            if key == "level_cap":
                level_cap[0].append(value[0])
                level_cap[1].append(value[1])

    # Calcule les niveaux et overflows des joueurs
    for player_index, player in enumerate(data):
        for skill in chain(skills, slayers):
            type_xp = "skill"
            category = "skills"
            max_level = None
            skill_list = skills

            if skill == "farming":
                max_level = level_cap[0][player_index] + 50
            if skill == "taming":
                max_level = level_cap[1][player_index] if level_cap[1][player_index] > 50 else 50
            if skill in ["fishing", "alchemy", "carpentry", "foraging"]:
                max_level = 50
            if skill == "dungeoneering":
                type_xp = "dungeon"
            if skill in slayers:
                type_xp = f"slayer_{skill}"
                category = "slayers"
                skill_list = slayers

            level, overflow = experience_to_level(
                type_xp, data[player][category][skill_list.index(skill)], max_level
            )
            ranking[skill]["level"][data[player]["pseudo"]] = level
            ranking[skill]["overflow"][data[player]["pseudo"]] = overflow

    # Trie les données du classement dans l'ordre décroissant
    sorted_ranking: dict = ranking.copy()
    for category in ranking:
        if isinstance(ranking[category], dict):
            # 'Level' et 'Networth'
            if category in ["level", "networth"]:
                sorted_ranking[category] = dict(
                    sorted(ranking[category].items(), key=lambda item: item[1], reverse=True)
                )
            # 'Skills' et 'slayers'
            if category in chain(skills, slayers):
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


def generate_ranking_message(data: dict, category: str, old_data: dict) -> list[str]:
    """Génère les messages pour les données du classement de la guilde sur Hypixel Skyblock.

    Args:
        data (dict): Les données du classement.
        category (str): La catégorie du classement.
        old_data (dict): Les anciennes données du classement pour faire la comparaison.

    Returns:
        list[str]: Les messages formatés.
    """
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
    # 'Level'
    if category == "level":
        for i, (player, value) in enumerate(data[category].items()):
            value = f"{value:.2f}"
            message = format_ranking_message(
                player, value, i, calculate_player_position(old_data, data, category, player)
            )
            messages.append(message)
    # 'Networth'
    if category == "networth":
        for i, (player, value) in enumerate(data[category].items()):
            value = format_number(value)
            message = format_ranking_message(
                player, value, i, calculate_player_position(old_data, data, category, player)
            )
            messages.append(message)
    # 'Skills' et 'slayers'
    if category in chain(skills_list, slayers_list):
        for i, (player, value) in enumerate(data[category]["level"].items()):
            overflow = data[category]["overflow"][player]
            if overflow:
                value = f"{value:.0f}"
                overflow = math.floor(overflow)
            else:
                value = f"{value:.2f}"
            message = format_ranking_message(
                player, value, i, calculate_player_position(old_data, data, category, player)
            )
            if overflow:
                message += f" (*{overflow:,}*)".replace(",", " ")
            messages.append(message)
    # 'Skill average'
    skills_avg: list[str] = skills_list.copy()
    skills_avg.remove("dungeoneering")
    if category == "skill average":
        # Calcule le 'skill average' pour les anciennes données
        for player in old_data[category]:
            total = []
            for skill in skills_avg:
                total.append(math.floor(old_data[skill]["level"][player]))
            average = math.fsum(total) / len(total)
            old_data[category][player] = average
        # Trie le 'skill average'
        old_data[category] = dict(
            sorted(old_data[category].items(), key=lambda item: item[1], reverse=True)
        )
        # Calcule le 'skill average' pour les nouvelles données
        for player in data[category]:
            total = []
            for skill in skills_avg:
                total.append(math.floor(data[skill]["level"][player]))
            average = math.fsum(total) / len(total)
            data[category][player] = average
        # Trie le 'skill average'
        data[category] = dict(
            sorted(data[category].items(), key=lambda item: item[1], reverse=True)
        )
        for i, (player, value) in enumerate(data[category].items()):
            value = f"{value:.2f}"
            message = format_ranking_message(
                player, value, i, calculate_player_position(old_data, data, category, player)
            )
            messages.append(message)
    return messages


def calculate_player_position(old_data: dict, new_data: dict, category: str, player: str) -> int:
    """Calcule la position d'un joueur dans le classement.

    Args:
        old_data (dict): Les anciennes données du classement.
        new_data (dict): Les nouvelles données du classement.
        category (str): La catégorie du classement.
        player (str): Le pseudo du joueur.

    Returns:
        int: -1 si le joueur a descendu, 0 s'il n'a pas bougé, 1 s'il a monté.
    """
    # 'Level', 'Networth' and 'Skill average'
    if category in ["level", "networth", "skill average"]:
        if player in old_data[category]:
            old_position = list(old_data[category].keys()).index(player)
            new_position = list(new_data[category].keys()).index(player)
            if new_position < old_position:
                return 1
            if new_position > old_position:
                return -1
        return 0
    # 'Skills' et 'slayers'
    if player in old_data[category]["level"]:
        old_position = list(old_data[category]["level"].keys()).index(player)
        new_position = list(new_data[category]["level"].keys()).index(player)
        if new_position < old_position:
            return 1
        if new_position > old_position:
            return -1
    return 0


async def display_ranking(img: str, old_ranking: dict) -> list[discord.Embed]:
    """Affiche le classement de la guilde sur Hypixel Skyblock. Si la taille dépasse la limite des embeds (5000 caractères),
    on crée plusieurs embeds.

    Args:
        img (str): L'URL de l'image à afficher en miniature.
        old_ranking (dict): Les anciennes données du classement pour faire la comparaison.

    Returns:
        list[discord.Embed]: La liste des embeds à afficher.
    """
    month = await month_to_str(date.today().month)
    year = date.today().year

    embeds_ranking = []
    ranking = discord.Embed(
        title=f"Classement de début {month} {year}",
        description="\N{NO ENTRY SIGN} LA NETWORTH N'EST PLUS CALCULÉE !\n"
        "Voici le classement de la guilde sur Hypixel Skyblock.\n"
        "Le skill average est sans progression (comme affiché sur Hypixel dans le menu des skills).",
        color=discord.Colour.from_rgb(0, 170, 255),
    )
    ranking.set_thumbnail(url=img)
    ranking.set_footer(text="\N{WHITE HEAVY CHECK MARK} Mis à jour le 1er de chaque mois à 8h00")
    new_ranking_data = parse_data(await load_skyblock())

    # On génère les messages pour chaque catégorie
    for category in new_ranking_data:
        if isinstance(new_ranking_data[category], dict):
            messages = generate_ranking_message(new_ranking_data, category, old_ranking)
            field_value = "\n".join(messages)
            # La limite des embeds est de 6000 caractères
            # on split avant de dépasser cette limite pour éviter une coupure dans les catégories
            if len(ranking) + len(field_value) > 5000:
                embeds_ranking.append(ranking)
                ranking = discord.Embed(
                    title=f"Classement de début {month} {year} - Suite",
                    description="\N{NO ENTRY SIGN} LA NETWORTH N'EST PLUS CALCULÉE !\n"
                    "Voici la suite du classement de la guilde sur Hypixel Skyblock.\n"
                    "Le skill average est sans progression (comme affiché sur Hypixel dans le menu des skills).",
                    color=discord.Colour.from_rgb(0, 170, 255),
                )
            # On ajoute les catégories dans les embeds
            ranking.add_field(
                name=f"**[ {category.capitalize()} ]**",
                value=field_value,
                inline=False,
            )
    # On ajoute la miniature ainsi que le footer aux autres embeds
    ranking.set_thumbnail(url=img)
    ranking.set_footer(text="\N{WHITE HEAVY CHECK MARK} Mis à jour le 1er de chaque mois à 8h00")
    embeds_ranking.append(ranking)
    return embeds_ranking
