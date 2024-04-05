import tomlkit

birthday_file_path = "data/birthdays.toml"


# Charge les anniversaires depuis un fichier TOML
def load_birthdays():
    try:
        with open(birthday_file_path) as f:
            return tomlkit.load(f)
    except FileNotFoundError:
        return {}


# Enregistre les anniversaires dans le fichier TOML
def save_birthdays(birthdays):
    with open(birthday_file_path, "w") as f:
        tomlkit.dump(birthdays, f)
