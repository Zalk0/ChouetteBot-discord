from discord.ext import tasks
from datetime import time
import discord.utils


def tasks_list(client):

    # Hours for the loop
    even_hours = [time(0), time(2), time(4), time(6), time(8), time(10),
                  time(12), time(14), time(16), time(18), time(20), time(22)]

    # Loop to send message every 2 hours for pokeroll
    @tasks.loop(time=even_hours)
    async def poke_ping():
        dresseurs = discord.Guild.get_role(client.get_guild(284980887634837504), 791365470837800992)
        pokeball = client.get_emoji(697018415646507078)
        msg_poke = f"{dresseurs.mention} C'est l'heure d'attraper des pokémons {pokeball}"
        await client.get_channel(768554688425492560).send(msg_poke)

    # Start loop
    poke_ping.start()
