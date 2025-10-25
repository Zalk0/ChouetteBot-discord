import logging
import os

import discord
from aiohttp import ClientSession, web

from chouette.commands_list import commands
from chouette.responses import responses
from chouette.tasks import tasks_list
from chouette.utils.version import get_version


class ChouetteBot(discord.Client):
    """Classe principale du bot ChouetteBot.

    Args:
        discord (Client): Instance de la classe Client de discord.py.
    """

    def __init__(self) -> None:
        """Initialise la classe ChouetteBot."""
        # Associate the env variables to the bot
        self.config = os.environ

        # Define the bot debug log level
        self.bot_logger = logging.getLogger("bot")
        log_level = logging.getLevelName(self.config.get("LOG_LEVEL", logging.INFO))
        self.log_level = log_level if isinstance(log_level, int) else logging.INFO
        self.bot_logger.setLevel(self.log_level)

        # Ignore RESUMED session messages
        logging.getLogger("discord.gateway").addFilter(
            lambda record: "successfully RESUMED session" not in record.msg
        )

        # Set intents for the bot
        intents = discord.Intents.all()
        intents.presences = False
        intents.typing = False
        intents.voice_states = False

        # Set activity of the bot
        activity_type = {
            "playing": 0,
            "streaming": 1,
            "listening": 2,
            "watching": 3,
            "custom": 4,  # IDK what it is
            "competing": 5,
        }
        activity = discord.Activity(
            type=activity_type.get(self.config["BOT_ACTIVITY_TYPE"]),
            name=self.config["BOT_ACTIVITY_NAME"],
        )

        # Apply intents, activity and status to the bot
        super().__init__(
            intents=intents,
            activity=activity,
            status=self.config["BOT_STATUS"],
        )

        # Declare command tree
        self.tree = discord.app_commands.CommandTree(self)

        # First declaration to be able to add commands to the guild
        self.hypixel_guild = discord.Object(int(self.config["HYPIXEL_GUILD_ID"]))

        # First declaration to be able to add commands to the guild
        self.my_guild = discord.Object(int(self.config["GUILD_ID"]))

    async def setup_hook(self) -> None:
        """Initialise le bot."""
        # Log the current running version
        self.bot_logger.info(await get_version())

        # Start aiohttp client session
        self.session = ClientSession()

        # Call commands and import tasks
        await commands(self)
        await tasks_list(self)

        # Start web server
        await self.start_server()

    async def on_ready(self) -> None:
        """Fonction appelée lorsque le bot est prêt."""
        # Waits until internal cache is ready
        await self.wait_until_ready()

        # Hypixel guild with all information
        self.hypixel_guild = self.get_guild(int(self.config["HYPIXEL_GUILD_ID"]))

        # My guild with all information
        self.my_guild = self.get_guild(int(self.config["GUILD_ID"]))

        # Log that the bot is ready and the number of guilds the bot is in
        self.bot_logger.info(f"{self.user} is now online and ready!")
        self.bot_logger.info(f"Number of servers I'm in : {len(self.guilds)}")

    async def on_message(self, message: discord.Message) -> None:
        """Fonction appelée lorsqu'un message est envoyé dans les salons auxquels il a accès.

        Args:
            message (discord.Message): Le message envoyé.
        """
        # Ignore messages from bots including self
        if message.author.bot:
            return

        # Store the message's information in variables
        author = message.author
        user_msg = message.content
        channel = message.channel

        # Do a log on the Python console
        if message.guild is not None:
            self.bot_logger.debug(
                f'{author} said: "{user_msg}" #{channel} in {message.guild.name}'
            )
        else:
            self.bot_logger.debug(f'{author} said: "{user_msg}" in Direct Message')

        # Call responses with message of the user and responds if necessary
        response = await responses(self, channel, user_msg, author)
        if response[0] != "":
            if response[1]:
                await channel.send(response[0], reference=message)
            else:
                await channel.send(response[0])
            self.bot_logger.info(f'{self.user} responded to {author}: "{response[0]}"')

    async def is_team_member_or_owner(self, author: discord.User) -> bool:
        """Vérifie si l'auteur est membre de l'équipe ou le propriétaire de l'application.

        Args:
            author (discord.User): L'utilisateur à vérifier.

        Returns:
            bool: `True` si l'utilisateur est membre de l'équipe ou le propriétaire, `False` sinon.
        """
        if self.application.team:
            return author.id in [member.id for member in self.application.team.members]
        return author.id == self.application.owner.id

    async def start_server(self) -> None:
        """Démarre un serveur HTTP pour vérifier si le bot est en ligne."""
        # Set a logger for the webserver
        web_logger = logging.getLogger("web")

        # Switch site access log to DEBUG level
        def access_filter(record: logging.LogRecord) -> bool:
            if record.levelno == logging.INFO:
                if self.log_level >= logging.INFO:
                    return False
                record.levelno = logging.DEBUG
                record.levelname = "DEBUG"
            return True

        logging.getLogger("aiohttp.access").addFilter(access_filter)

        # Set some basic headers for security
        headers = {
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
        }

        # Remove the Server header and apply the headers
        async def _default_headers(req: web.Request, res: web.StreamResponse) -> None:
            """Applique les headers par défaut à la réponse."""
            if "Server" in res.headers:
                del res.headers["Server"]
            res.headers.update(headers)

        # This is the response
        async def handler(req: web.Request) -> web.Response:
            """Réponse du serveur web."""
            return web.Response(text=f"{self.user.name} is up")

        app = web.Application()
        app.on_response_prepare.append(_default_headers)
        app.add_routes([web.get("/", handler)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self.config["SERVER_HOST"], int(self.config["SERVER_PORT"]))
        try:
            await site.start()
        except Exception as e:
            web_logger.warning(f"Error while starting the webserver: \n{e}")
        else:
            web_logger.info("The webserver has successfully started")

    async def close(self) -> None:
        """Ferme le bot et libère les ressources."""
        # Close aiohttp client session
        self.bot_logger.debug("Closing the aiohttp client session")
        await self.session.close()

        # Do normal close
        await super().close()
        self.bot_logger.info("Bot stopped gracefully")
