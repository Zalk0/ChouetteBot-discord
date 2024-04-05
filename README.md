# ChouetteBot-discord

[![Ruff status](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/ruff.yaml/badge.svg?branch=main)](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/ruff.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Zalk0/ChouetteBot-discord/main.svg)](https://results.pre-commit.ci/latest/github/Zalk0/ChouetteBot-discord/main)

Just some random project of doing a Discord bot using
[discord.py](https://github.com/Rapptz/discord.py).  
You need to have Python 3.8 or higher installed (required by discord.py)!

Clone the projet and install the requirements (preferably in a
[venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments)):

```bash
git clone git@github.com:Zalk0/ChouetteBot-discord.git
cd ChouetteBot-discord
pip install -r requirements.txt
```

---
Before launching the bot, you need to fill in a **`.env`** file (using the
[template](https://github.com/Zalk0/ChouetteBot-discord/blob/main/.env.example)
I provide in the repo) and put a Discord bot token inside.  
To have one, go to the
[Discord Developer Portal](https://discord.com/developers) and create a new
application.  
Go to the Bot section and click the Reset Token button, you can now claim the
token.  
You need to enable the message content and members Privileged Gateway Intents as I assume
they're enabled in the code (or change them).  
You also have to fill the other fields in your `.env` file or else you're going to have errors.

---
After having done all this you can launch the bot :

```bash
python main.py
```

---

### Docker

[![Docker Image](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/docker-image.yaml/badge.svg?branch=main)](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/docker-image.yaml)

You can use a Docker image to deploy the bot. It's currently supporting amd64, armv6 and armv7
architectures. We provide deployment information on the [Docker Hub repository](https://hub.docker.com/r/gylfirst/chouettebot).
