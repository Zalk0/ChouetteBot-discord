from datetime import date, datetime
from pathlib import Path

from chouette.utils.data_io import data_read, data_write

BIRTHDAY_FILE = Path("data", "birthdays.toml")


async def load_birthdays() -> dict:
    """Charge les anniversaires depuis un fichier TOML depuis le disque."""
    return await data_read(BIRTHDAY_FILE)


async def save_birthdays(birthdays: dict) -> None:
    """Sauvegarde les anniversaires dans un fichier TOML sur le disque."""
    await data_write(birthdays, BIRTHDAY_FILE)


async def check_date(day: int, month: int, year: int) -> date:
    """Vérifie si la date est valide et la retourne."""
    if not year:
        return date(4, month, day)
    if year < 1900 or year > date.today().year:
        raise ValueError
    return date(year, month, day)


async def calculate_age(year: int) -> int | None:
    """Calcule l'âge de la personne en fonction de son année de naissance."""
    return date.today().year - year if year != 4 else None


async def datetime_to_timestamp(birthday: date) -> str:
    """Convertit une date donnée en timestamp Discord."""
    birthday_dt = datetime.fromisoformat(str(birthday))
    unix_timestamp = birthday_dt.timestamp()
    return f"<t:{int(unix_timestamp)}:R>"


async def month_to_str(month: int) -> str:
    """Convertit un numéro de mois en français."""
    months: list[str] = [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ]
    return months[month - 1]
