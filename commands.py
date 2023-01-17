import discord
import random


def commands_list(client, tree):

    # Make the roll command
    @tree.command(name="roll", description="Roll a die")
    async def die_roll(interaction: discord.Interaction):
        await interaction.response.send_message(f"{random.randint(1, 6)} \N{GAME DIE}")

    # Make the ping command
    @tree.command(name="ping", description="Test the ping of the bot")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! In {round(client.latency * 1000)}ms")

    # Make a cheh command
    @tree.command(name="cheh", description="Cheh somebody")
    async def cheh(interaction: discord.Interaction, user: discord.Member):
        # Check if the user to cheh is the bot
        if user == client.user:
            await interaction.response.send_message("Vous ne pouvez pas me **Cheh** !")
        elif user == interaction.user:
            await interaction.response.send_message("**FEUR**")
        else:
            cheh_gif = "https://tenor.com/view/cheh-true-cheh-gif-19162969"
            await interaction.response.send_message(f"Cheh {user.mention}")
            await interaction.channel.send(cheh_gif)

    # Make a simple context menu application
    @tree.context_menu(name="Hello")
    async def hello(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(f"Hey! {interaction.user.mention}")

    # Make a context menu command to delete messages
    # @tree.context_menu(name="Delete until here")
    # async def delete(interaction: discord.Interaction, message: discord.Message):
    #     if not interaction.permissions.manage_messages:
    #         await interaction.response.send_message(f"Vous n'avez pas la permission de gérer les messages !", ephemeral=True)
    #         return
    #     await interaction.response.send_message("En train de supprimer les messages...", ephemeral=True, delete_after=0)
    #     def is_msg(msg):
    #         return msg.id >= message.id
    #     del_msg = await message.channel.purge(check=is_msg, reason="Admin used bulk delete")
    #     await interaction.channel.send(f"{len(del_msg)} messages supprimés !", delete_after=10)
