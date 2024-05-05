from datetime import date, datetime
from pathlib import Path

from chouette.utils.data_io import data_read, data_write

BIRTHDAY_FILE = Path("data", "birthdays.toml")


# Function to load the birthday file
async def load_birthdays() -> dict:
    return await data_read(BIRTHDAY_FILE)


# Save birthdays in a TOML file
async def save_birthdays(birthdays: dict):
    await data_write(birthdays, BIRTHDAY_FILE)


# Function to verify if the given year is valid
async def check_date(day: int, month: int, year: int) -> date:
    if not year:
        return date(4, month, day)
    if year < 1900 or year > date.today().year:
        raise ValueError
    return date(year, month, day)


# Function to calculate the age
async def calculate_age(year: int) -> int:
    return date.today().year - year if year != 4 else None


# Function to convert a datetime object to Discord timestamp
async def datetime_to_timestamp(birthday: date) -> str:
    birthday_dt = datetime.fromisoformat(str(birthday))
    unix_timestamp = birthday_dt.timestamp()
    return f"<t:{int(unix_timestamp)}:R>"
