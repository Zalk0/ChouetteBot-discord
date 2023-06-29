from bot import ChouetteBot


def main():
    # Create an instance of the SimpleBot
    client = ChouetteBot()

    # Run the client with the token
    client.run(client.config['BOT_TOKEN'], reconnect=True)


if __name__ == '__main__':
    main()
