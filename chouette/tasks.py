from __future__ import annotations

from datetime import date, time, timedelta
from os import getenv
from typing import TYPE_CHECKING

from discord.errors import DiscordServerError
from discord.ext import tasks

from chouette.utils.birthdays import calculate_age, load_birthdays
from chouette.utils.skyblock import SkyblockUtils

if TYPE_CHECKING:
    from chouette.bot import ChouetteBot

# Get local timezone for tasks
try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

    TIMEZONE = ZoneInfo(getenv("TZ", "localtime"))
# Use timezone UTC as a fallback
except ZoneInfoNotFoundError:
    from datetime import UTC

    TIMEZONE = UTC


async def tasks_list(client: ChouetteBot) -> None:
    """Liste des tâches à effectuer pour le bot."""
    sb_utils = SkyblockUtils(client)

    # Send message every 2 hours for pokeroll in utc time (default)
    @tasks.loop(time=[time(t) for t in range(0, 24, 2)])
    async def poke_ping() -> None:
        """Envoie un message pour le pokeroll."""
        guild = client.get_guild(int(client.config["GUILD_ID"]))
        dresseurs = guild.get_role(int(client.config["POKE_ROLE"]))
        pokeball = client.get_emoji(int(client.config["POKEBALL_EMOJI"]))
        msg_poke = f"{dresseurs.mention} C'est l'heure d'attraper des pokémons {pokeball}"
        await client.get_channel(int(client.config["POKE_CHANNEL"])).send(msg_poke)

    # Check if it's someone's birthday every day at 8am in local time
    @tasks.loop(time=time(8, tzinfo=TIMEZONE))
    async def check_birthdays() -> None:
        """Vérifie si c'est l'anniversaire de quelqu'un."""
        guild = client.get_guild(int(client.config["GUILD_ID"]))
        role = guild.get_role(int(client.config["BIRTHDAY_ROLE"]))
        for member in role.members:
            await member.remove_roles(role, reason="Birthday ended")
        for user_id, info in (await load_birthdays(client.data_io)).items():
            birthday: date = info.get("birthday")
            if (birthday.day == date.today().day and birthday.month == date.today().month) or (
                birthday.day == 29
                and birthday.month == 2
                and date.today() - timedelta(days=1) == date(date.today().year, 2, 28)
            ):
                user = guild.get_member(int(user_id))
                await user.add_roles(role, reason="Birthday")
                age = await calculate_age(birthday.year)
                if age:
                    msg_birthday = (
                        f"\N{PARTY POPPER} {user.display_name} a maintenant un an de plus !\n"
                        f"Il/Elle a maintenant {age} ans \N{BIRTHDAY CAKE}\n"
                        "Souhaitez-lui un joyeux anniversaire ! \N{PARTY POPPER}"
                    )
                else:
                    msg_birthday = (
                        f"\N{PARTY POPPER} {user.display_name} a maintenant un an de plus !\n"
                        "Souhaitez-lui un joyeux anniversaire ! \N{PARTY POPPER}"
                    )
                await client.get_channel(int(client.config["BIRTHDAY_CHANNEL"])).send(msg_birthday)

    # Display the ranking for Hypixel Skyblock guild every month on the 1st at 8am in local time
    @tasks.loop(time=time(8, tzinfo=TIMEZONE))
    async def skyblock_guild_ranking() -> None:
        """Affiche le classement de la guilde Hypixel Skyblock."""
        if date.today().day == 1:
            await sb_utils.ranking.guild_ranking()

    # Start loops
    poke_ping.start()
    check_birthdays.start()
    skyblock_guild_ranking.start()

    @poke_ping.error
    @check_birthdays.error
    @skyblock_guild_ranking.error
    async def on_task_error(error: BaseException) -> None:
        """Gère les erreurs lors de l'exécution des taches.

        Args:
            error (BaseException): L'erreur qui a été levée.
        """
        client.bot_logger.error(f"Error while executing a task:\n{error}")
        if isinstance(error, DiscordServerError):
            if poke_ping.failed():
                poke_ping.restart()
                client.bot_logger.info("poke_ping task has been restarted")
            if check_birthdays.failed():
                check_birthdays.restart()
                client.bot_logger.info("check_birthdays task has been restarted")
            if skyblock_guild_ranking.failed():
                skyblock_guild_ranking.restart()
                client.bot_logger.info("skyblock_guild_ranking task has been restarted")
