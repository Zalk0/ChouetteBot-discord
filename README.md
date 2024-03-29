# ChouetteBot-discord

[![Ruff](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/ruff.yaml/badge.svg)](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/ruff.yaml)

Just some random project of doing a Discord bot
using [discord.py](https://github.com/Rapptz/discord.py).  
You need to have Python 3.8 or higher installed (required by discord.py) !

Clone the projet and install the requirements (preferably in
a [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments)) :

```
git clone git@github.com:Zalk0/ChouetteBot-discord.git
cd ChouetteBot-discord
pip install -r requirements.txt
```

---
Before launching the bot, you need to fill in a **`.env`** file (using
the [template](https://github.com/Zalk0/ChouetteBot-discord/blob/main/.env.example)
I provide in the repo) and put a Discord bot token inside.  
To have one, go to
the [Discord Developer Portal](https://discord.com/developers) and create a new
application.  
Go to the Bot section and click the Reset Token button, you can now claim the
token.  
You also have to enable all the Privileged Gateway Intents as I assume they're
enabled in the code (or change them).

---
After having done all this you can launch the bot :

```
python main.py
```

---
### Docker
[![Docker Image](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/docker-image.yml)

You can use the docker image to deploy the bot. It's currently supporting amd64 and armv6 architectures. We provide deployement informations on the docker hub repository.

[Docker Hub](https://hub.docker.com/r/gylfirst/chouettebot)