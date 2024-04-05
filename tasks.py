from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING

from discord.ext import tasks

if TYPE_CHECKING:
    from bot import ChouetteBot


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
    @tasks.loop(hours=24)
    async def check_birthdays():
        now = time.now()
        if now.hour == 8 and now.minute == 0:
            today = now.strftime("%d/%m")
            for user_id, birthday in birthdays.items():
                if birthday == today:
                    user = await bot.fetch_user(int(user_id))
                    msg_birthday = f":tada: {user.mention} is a year older now! Wish them a happy birthday! :tada:"
                    await client.get_channel(int(client.config["BIRTHDAY_CHANNEL"])).send(
                        msg_birthday
                    )

    # Start loop
    poke_ping.start()
    check_birthdays.start()
