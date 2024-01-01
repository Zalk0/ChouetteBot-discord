import logging
import os

import discord
from aiohttp import web

import tasks
from commands_list import commands
from responses import responses


# Create a class of the bot
class ChouetteBot(discord.Client):
    # Initialization when class is called
    def __init__(self):
        # Associate the env variables to the bot
        self.config = os.environ

        # Define the bot debug log level
        self.bot_logger = logging.getLogger("bot")
        log_level = logging.getLevelName(self.config.get("LOG_LEVEL", logging.INFO))
        self.log_level = log_level if isinstance(log_level, int) else logging.INFO
        self.bot_logger.setLevel(self.log_level)

        # Ignore RESUMED session messages
        logging.getLogger("discord.gateway").addFilter(
            lambda record: "successfully RESUMED session" in record.msg
        )

        # Set intents for the bot
        intents = discord.Intents.all()

        # Set activity of the bot
        activity_type = {
            "playing": 0,
            "streaming": 1,
            "listening": 2,
            "watching": 3,
            "custom": 4,  # Idk what it is
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

        # Variable for storing owners id
        # If set manually, it will not fetch from the bot's application info
        self.owners = []

        # Used to check the first time the bot does the on_ready event
        self.first = True

    # Wait until bot is ready
    async def on_ready(self):
        # Waits until internal cache is ready
        await self.wait_until_ready()

        # Executed once when bot is ready
        if self.first:
            # Hypixel guild
            hypixel_guild = self.get_guild(int(self.config["HYPIXEL_GUILD_ID"]))

            # Call commands and import tasks
            await commands(self.tree, hypixel_guild)
            await tasks.tasks_list(self)

            # Start web server
            await self.start_server()

            self.first = False

        # Check the number of servers the bot is a part of
        self.bot_logger.info(f"Number of servers I'm in : {len(self.guilds)}")

        # Log in the console that the bot is ready
        self.bot_logger.info(f"{self.user} is now online and ready!")

    # To react to messages sent in channels bot has access to
    async def on_message(self, message: discord.Message):
        # Ignore messages from bots including self
        if message.author.bot:
            return

        # Stock the message's informations in variables
        author = message.author
        user_msg = str(message.content)
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
        if not response[0] == "":
            if response[1]:
                await channel.send(response[0], reference=message)
            else:
                await channel.send(response[0])
            self.bot_logger.info(f'{self.user} responded to {author}: "{response[0]}"')

    async def is_team_member_or_owner(self, author: discord.User) -> bool:
        if not self.owners:
            app_info = await self.application_info()
            if app_info.team:
                self.owners = [member.id for member in app_info.team.members]
            else:
                self.owners = [app_info.owner.id]
        return author.id in self.owners

    # Add a basic HTTP server to check if the bot is up
    async def start_server(self):
        # Set a logger for the webserver
        web_logger = logging.getLogger("web")
        # Don't want to spam logs with site access
        if self.log_level >= logging.INFO:
            logging.getLogger("aiohttp.access").setLevel(logging.ERROR)

        # Set some basic headers for security
        headers = {
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
        }

        # Remove the Server header and apply the headers
        async def _default_headers(req: web.Request, res: web.StreamResponse):
            if "Server" in res.headers:
                del res.headers["Server"]
            res.headers.update(headers)

        # This is the response
        async def handler(req: web.Request):
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
