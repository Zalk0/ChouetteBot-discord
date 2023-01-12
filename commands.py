import discord
import random
from discord.ext import tasks
from datetime import time


def commands_list(client, tree):

    # Hours for the loop
    even_hours = [time(0), time(2), time(4), time(6), time(8), time(10),
                  time(12), time(14), time(16), time(18), time(20), time(22)]

    # Loop to send message every 2 hours for pokeroll
    @tasks.loop(time=even_hours)
    async def poke_ping(ctx):
        dresseurs = discord.utils.get(ctx.guild.roles, id=791365470837800992)
        pokeball = client.get_emoji(697018415646507078)
        msg_poke = f"{dresseurs.mention} C'est l'heure d'attraper des pokémons {pokeball}"
        await client.get_channel(768554688425492560).send(msg_poke)

    # Pokehunt ping
    @tree.command(name="pokehunt", description="Command to launch pings for pokemons hunters")
    async def poke(ctx, option: str):
        if option == "enable":
            if not poke_ping.is_running():
                poke_ping.start(ctx)
                await ctx.response.send_message("Le pokeping a bien été activé !", ephemeral=True)
            else:
                await ctx.response.send_message("Le pokeping est déjà activé", ephemeral=True)
        if option == "disable":
            if poke_ping.is_running():
                poke_ping.stop()
                await ctx.response.send_message("Le pokeping a été désactivé", ephemeral=True)
            else:
                await ctx.response.send_message("Le pokeping est déjà désactivé !", ephemeral=True)
        if option == "status":
            if poke_ping.is_running():
                await ctx.response.send_message("Le pokeping est activé", ephemeral=True)
            else:
                await ctx.response.send_message("Le pokeping est désactivé", ephemeral=True)

    # Autocompletion for pokehunt options
    @poke.autocomplete("option")
    async def poke_option_autocomplete(ctx, current: str) -> list[discord.app_commands.Choice[str]]:
        options = ["enable", "disable", "status"]
        return [discord.app_commands.Choice(name=option, value=option)
                for option in options if current.lower() in option.lower()]

    # Make the roll command
    @tree.command(name="roll", description="Roll a die")
    async def die_roll(interaction: discord.Interaction):
        await interaction.response.send_message(f"{random.randint(1, 6)} \N{GAME DIE}")

    # Make the ping command
    @tree.command(name="ping", description="Test the ping of the bot")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! In {round(client.latency * 1000)}ms")

    # Make a simple context menu application
    @tree.context_menu(name="Hello")
    async def hello(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(f"Hey! {interaction.user.mention}")

    # Make a context menu command to delete messages
    # @tree.context_menu(name="Delete until here")
    # async def delete(interaction: discord.Interaction, message: discord.Message):
    #     def is_msg(msg):
    #         return msg.id == message.id
    #     del_msg = await discord.TextChannel.purge(client, check=is_msg, bulk=True, reason="Admin used bulk delete")
    #     await interaction.response.send_message(f"{del_msg} messages deleted!", ephemeral=True)
    # exception: AttributeError: 'YoloBot' object has no attribute 'history'
