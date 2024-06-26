import logging.handlers as handlers
from pathlib import Path

from dotenv import load_dotenv

from chouette.bot import ChouetteBot


def main() -> None:
    """Fonction principale du bot."""
    # Load the .env values if a .env file exists
    if Path(".env").is_file():
        load_dotenv()

    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)

    # Create an instance of the ChouetteBot
    client = ChouetteBot()

    # Setup the logging
    Path("logs").mkdir(exist_ok=True)
    handler = handlers.RotatingFileHandler(
        filename=Path("logs", "bot.log"),
        backupCount=3,
        encoding="utf-8",
        delay=True,
    )
    handler.doRollover()

    # Run the client with the token
    client.run(
        client.config["BOT_TOKEN"],
        reconnect=True,
        log_handler=handler,
        root_logger=True,
    )


if __name__ == "__main__":
    main()
