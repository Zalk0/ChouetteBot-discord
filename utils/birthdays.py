import asyncio
from datetime import date
from pathlib import Path

import tomlkit

Path("data").mkdir(exist_ok=True)
BIRTHDAY_FILE = Path("data", "birthdays.toml")
FILE_LOCK = asyncio.Lock()


# Charge les anniversaires depuis un fichier TOML
async def load_birthdays() -> dict:
    async with FILE_LOCK:
        return await asyncio.get_event_loop().run_in_executor(None, _file_read)


def _file_read():
    try:
        with open(BIRTHDAY_FILE) as f:
            return tomlkit.load(f)
    except FileNotFoundError:
        return {}


# Enregistre les anniversaires dans le fichier TOML
async def save_birthdays(birthdays: dict):
    async with FILE_LOCK:
        await asyncio.get_event_loop().run_in_executor(None, _file_write, birthdays)


def _file_write(birthdays: dict):
    with open(BIRTHDAY_FILE, "w") as f:
        tomlkit.dump(birthdays, f)


# Permet de vérifier si la valeur est correcte
async def check_date(day: int, month: int, year: int) -> date:
    if not year:
        return date(4, month, day)
    if year < 1900 or year > date.today().year:
        raise ValueError
    return date(year, month, day)


# Permet de calculer l'âge
async def calculate_age(year: int) -> int:
    return date.today().year - year if year != 4 else None
