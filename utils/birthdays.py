from datetime import date
from pathlib import Path

import tomlkit

Path("data").mkdir(exist_ok=True)
BIRTHDAY_FILE = Path("data", "birthdays.toml")


# Charge les anniversaires depuis un fichier TOML
def load_birthdays() -> dict:
    try:
        with open(BIRTHDAY_FILE) as f:
            return tomlkit.load(f)
    except FileNotFoundError:
        return {}


# Enregistre les anniversaires dans le fichier TOML
def save_birthdays(birthdays: dict):
    with open(BIRTHDAY_FILE, "w") as f:
        tomlkit.dump(birthdays, f)


# Permet de vérifier si la valeur est correcte
async def check_year_value(year: int) -> int:
    if not year:
        return 1
    if year < 1900 or year > date.today().year:
        raise ValueError
    return year


# Permet de calculer l'âge
async def calculate_age(year: int) -> int:
    return date.today().year - year if year != 1 else None
