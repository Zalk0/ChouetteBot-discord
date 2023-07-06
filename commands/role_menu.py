import discord
from discord import app_commands
from emoji import is_emoji


# Define a RoleButton class
class RoleButton(discord.ui.Button):
    # Init button with label and custom id
    def __init__(self, role: discord.Role, emoji: str, style: discord.ButtonStyle):
        super().__init__(label=role.name, custom_id=f"{role.name.lower().replace(' ', '_')}_btn",
                         emoji=emoji, style=style)
        self.role = role

    # Set what to do if interaction
    async def callback(self, interaction: discord.Interaction):
        if self.role in interaction.user.roles:
            await interaction.user.remove_roles(self.role)
            await interaction.response.send_message(f"Vous n'avez plus le rôle {self.role.name} !", ephemeral=True)
        else:
            await interaction.user.add_roles(self.role)
            await interaction.response.send_message(f"Vous avez maintenant le rôle {self.role.name} !", ephemeral=True)


# Define a View class
class View(discord.ui.View):
    def __init__(self, buttons: list):
        super().__init__(timeout=None)
        for button in buttons:
            self.add_item(button)


# Define command group based on the Group class
class RoleMenu(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(name="role_menu", description="Role menu commands")
        self.buttons = None

    # Make command to initialize a role menu
    @app_commands.command(name="init", description="Initialize a role menu")
    async def init(self, interaction: discord.Interaction):
        self.buttons = []
        await interaction.response.send_message("Le menu de rôles a été initialisé.\n"
                                                "Vous pouvez maintenant utiliser la commande **/role_menu add**.",
                                                ephemeral=True)

    # Make command to add a role to a menu being created
    @app_commands.command(name="add", description="Add a role to a menu being created")
    async def add(self, interaction: discord.Interaction, role: discord.Role,
                  emoji: str, style: discord.ButtonStyle):
        # Check if self.buttons is initialized
        if self.buttons is None:
            await interaction.response.send_message("Le menu de rôles n'a pas été initialisé, utilisez "
                                                    "d'abord la commande **/role_menu init**", ephemeral=True)
            return
        # Check if self.buttons has not exceded the max
        if len(self.buttons) == 25:
            await interaction.response.send_message("Il y a déjà 25 boutons, c'est le maximum !", ephemeral=True)
            return
        # Check if the emoji entered is valid
        if not is_emoji(emoji):
            await interaction.response.send_message("L'emoji entré n'est pas valide", ephemeral=True)
            return
        # Check if the role was not already added
        for button in self.buttons:
            if role.name == button.label:
                await interaction.response.send_message("Un bouton contenant ce rôle est déjà dans ce menu",
                                                        ephemeral=True)
                return
        self.buttons.append(RoleButton(role, emoji, style))
        await interaction.response.send_message(f"Le rôle {role.name} a bien été ajouté au menu.", ephemeral=True)

    # Make command to create the role menu, display it and save message ID
    @app_commands.command(name="create", description="Create the role menu with roles entered")
    async def create(self, interaction: discord.Interaction):
        # Check if self.buttons is initialized
        if self.buttons is None:
            await interaction.response.send_message("Le menu de rôles n'a pas été initialisé, utilisez "
                                                    "d'abord la commande **/role_menu init**", ephemeral=True)
            return
        view = View(self.buttons)
        # Reset self.buttons
        self.buttons = None
        role_menu = await interaction.channel.send("Cliquez sur le bouton correspondant au rôle voulu :", view=view)
        await interaction.response.send_message(f"Le menu de rôles a été créé (ID : {role_menu.id})", ephemeral=True)

    # TODO : solve only one menu can be created at a time on any server
    # TODO : Need to save id to file so that bot can still interact after reboot
