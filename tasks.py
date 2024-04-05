from __future__ import annotations

from datetime import date, time
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from discord.ext import tasks

from utils import birthdays

if TYPE_CHECKING:
    from bot import ChouetteBot

TIMEZONE = ZoneInfo("localtime")


async def tasks_list(client: ChouetteBot):
    # Loop to send message every 2 hours for pokeroll
    @tasks.loop(time=[time(t) for t in range(0, 24, 2)])
    async def poke_ping():
        guild = client.get_guild(int(client.config["GUILD_ID"]))
        dresseurs = guild.get_role(int(client.config["POKE_ROLE"]))
        pokeball = client.get_emoji(int(client.config["POKEBALL_EMOJI"]))
        msg_poke = f"{dresseurs.mention} C'est l'heure d'attraper des pokémons {pokeball}"
        await client.get_channel(int(client.config["POKE_CHANNEL"])).send(msg_poke)

    # Loop to check if it's 8:00 and send a message if it's someone's birthday
    @tasks.loop(time=time(8, tzinfo=TIMEZONE))
    async def check_birthdays():
        for user_id, birthday in birthdays.load_birthdays():
            if birthday == date.today():
                user = client.get_user(user_id)
                # TODO: add age if user has given year of birth
                msg_birthday = (
                    f"\N{PARTY POPPER} {user.mention} is a year older now!"
                    "Wish them a happy birthday! \N{PARTY POPPER}"
                )
                await client.get_channel(int(client.config["BIRTHDAY_CHANNEL"])).send(msg_birthday)

    # Start loop
    poke_ping.start()
    check_birthdays.start()
