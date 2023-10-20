# ChouetteBot-discord

[![Python lint](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/Zalk0/ChouetteBot-discord/actions/workflows/python-app.yml)

Just some random project of doing a Discord bot using [discord.py](https://github.com/Rapptz/discord.py).  
You need to have Python 3.11 because I use a function that was introduced in this version (in the logging library) !

Clone the projet and install the requirements :

```
git clone https://github.com/Zalk0/ChouetteBot-discord.git
cd ChouetteBot-discord
pip install -r requirements.txt
```

---
Before launching the bot, you need to fill in a **`.env`** file (using the [template](https://github.com/Zalk0/ChouetteBot-discord/blob/main/.env.example)
I provide in the repo) and put a Discord bot token inside.  
To have one, go to the [Discord Developer Portal](https://discord.com/developers) and create a new application.  
Go to the Bot section and click the Reset Token button, you can now claim the token.  
You also have to enable all the Privileged Gateway Intents as I assume they're enabled in the code.

---
After having done all this you can launch the bot :

```
python main.py
```
