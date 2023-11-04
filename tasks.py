from datetime import time

from discord.ext import tasks


async def tasks_list(client):
    # Hours for the loop
    even_hours = [time(0), time(2), time(4), time(6), time(8), time(10),
                  time(12), time(14), time(16), time(18), time(20), time(22)]

    # Loop to send message every 2 hours for pokeroll
    @tasks.loop(time=even_hours)
    async def poke_ping():
        guild = client.get_guild(int(client.config['GUILD_ID']))
        dresseurs = guild.get_role(int(client.config['POKE_ROLE']))
        pokeball = client.get_emoji(int(client.config['POKEBALL_EMOJI']))
        msg_poke = f"{dresseurs.mention} C'est l'heure d'attraper des pokémons {pokeball}"
        await client.get_channel(int(client.config['POKE_CHANNEL'])).send(msg_poke)

    # Start loop
    poke_ping.start()
