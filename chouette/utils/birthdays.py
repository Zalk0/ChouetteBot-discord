from datetime import date, datetime
from pathlib import Path

from chouette.utils.data_io import data_read, data_write

BIRTHDAY_FILE = Path("data", "birthdays.toml")


async def load_birthdays() -> dict:
    """Charge les anniversaires depuis un fichier TOML sur le disque.

    Returns:
        dict: Les anniversaires chargés depuis le fichier.
    """
    return await data_read(BIRTHDAY_FILE)


async def save_birthdays(birthdays: dict) -> None:
    """Sauvegarde les anniversaires dans un fichier TOML sur le disque.

    Args:
        birthdays (dict): Les anniversaires à sauvegarder.
    """
    await data_write(birthdays, BIRTHDAY_FILE)


async def check_date(day: int, month: int, year: int) -> date:
    """Vérifie si la date est valide et la retourne.

    Args:
        day (int): Le jour de la date.
        month (int): Le mois de la date.
        year (int): L'année de la date.

    Raises:
        ValueError: Si la date n'est pas valide.

    Returns:
        date: La date vérifiée.
    """
    if not year:
        return date(4, month, day)
    if year < 1900 or year > date.today().year:
        raise ValueError("L'année doit être comprise entre 1900 et l'année en cours.")
    return date(year, month, day)


async def calculate_age(year: int) -> int | None:
    """Calcule l'âge de la personne en fonction de son année de naissance.

    Args:
        year (int): L'année de naissance de la personne.

    Returns:
        int | None: L'âge de la personne ou `None` si l'année est invalide.
    """
    return date.today().year - year if year != 4 else None


async def datetime_to_timestamp(birthday: date) -> str:
    """Convertit une date en timestamp Discord.

    Args:
        birthday (date): La date à convertir.

    Returns:
        str: Le timestamp Discord correspondant.
    """
    birthday_dt = datetime.fromisoformat(str(birthday))
    unix_timestamp = birthday_dt.timestamp()
    return f"<t:{int(unix_timestamp)}:R>"


async def month_to_str(month: int) -> str:
    """Convertit un numéro de mois en français.

    Args:
        month (int): Le numéro du mois (1-12).

    Returns:
        str: Le nom du mois en français.
    """
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
