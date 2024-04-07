from __future__ import annotations

from datetime import date, time
from os import getenv
from typing import TYPE_CHECKING

from discord.ext import tasks

from utils.birthdays import calculate_age, load_birthdays

if TYPE_CHECKING:
    from bot import ChouetteBot

# Get local timezone for tasks
try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

    TIMEZONE = ZoneInfo(getenv("TZ", "localtime"))
# Use timezone UTC as a fallback
except ZoneInfoNotFoundError:
    from datetime import timezone

    TIMEZONE = timezone.utc


async def tasks_list(client: ChouetteBot):
    # Loop to send message every 2 hours for pokeroll in utc time (default)
    @tasks.loop(time=[time(t) for t in range(0, 24, 2)])
    async def poke_ping():
        guild = client.get_guild(int(client.config["GUILD_ID"]))
        dresseurs = guild.get_role(int(client.config["POKE_ROLE"]))
        pokeball = client.get_emoji(int(client.config["POKEBALL_EMOJI"]))
        msg_poke = f"{dresseurs.mention} C'est l'heure d'attraper des pokémons {pokeball}"
        await client.get_channel(int(client.config["POKE_CHANNEL"])).send(msg_poke)

    # Loop to check if it's someone's birthday every day at 8am in local time
    @tasks.loop(time=time(8, tzinfo=TIMEZONE))
    async def check_birthdays():
        guild = client.get_guild(int(client.config["GUILD_ID"]))
        role = guild.get_role(int(client.config["BIRTHDAY_ROLE"]))
        for member in role.members:
            await member.remove_roles(role)
        for user_id, info in (await load_birthdays()).items():
            birthday: date = info.get("birthday")
            if birthday == date.today().replace(birthday.year):
                user = guild.get_member(int(user_id))
                await user.add_roles(role, reason="Birthday")
                age = await calculate_age(birthday.year)
                if age:
                    msg_birthday = (
                        f"\N{PARTY POPPER} {user.mention} is a year older now!\n"
                        f"{user.display_name} is now {age} \N{BIRTHDAY CAKE}\n"
                        "Wish them a happy birthday! \N{PARTY POPPER}"
                    )
                else:
                    msg_birthday = (
                        f"\N{PARTY POPPER} {user.mention} is a year older now!\n"
                        "Wish them a happy birthday! \N{PARTY POPPER}"
                    )
                await client.get_channel(int(client.config["BIRTHDAY_CHANNEL"])).send(msg_birthday)

    # Start loop
    poke_ping.start()
    check_birthdays.start()
