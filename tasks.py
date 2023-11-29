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
        await client.get_channel(int(client.config["POKE_CHANNEL"])).send(
            msg_poke
        )

    # Start loop
    poke_ping.start()
