import logging.handlers as handlers
import os

from bot import ChouetteBot


def main():
    # Create an instance of the ChouetteBot
    client = ChouetteBot()

    # Setup the logging
    os.makedirs('logs', exist_ok=True)
    handler = handlers.RotatingFileHandler(filename='logs\\bot.log', encoding='utf-8', backupCount=3)
    handler.doRollover()

    # Run the client with the token
    client.run(client.config['BOT_TOKEN'], reconnect=True, root_logger=True, log_handler=handler)


if __name__ == '__main__':
    main()
