from asyncio import Lock, to_thread
from pathlib import Path

import tomlkit

FILE_LOCKS = {}


def _get_lock(file: Path) -> Lock:
    """Retourne le verrou associé à un chemin et le crée s'il n'existe pas.

    Args:
        file (Path): Le chemin du fichier.

    Returns:
        Lock: Le verrou associé au chemin.
    """
    for path, lock in FILE_LOCKS.items():
        if path == file:
            return lock
    FILE_LOCKS.update({file: Lock()})
    return FILE_LOCKS.get(file)


def _file_read(file: Path) -> dict:
    """Lit un fichier TOML et retourne un dictionnaire.

    Args:
        file (Path): Le chemin du fichier.

    Returns:
        dict: Le dictionnaire lu depuis le fichier.
    """
    try:
        return tomlkit.parse(file.read_text())
    except FileNotFoundError:
        return {}


async def data_read(file: Path) -> dict:
    """Lit un fichier TOML et retourne un dictionnaire.

    Args:
        file (Path): Le chemin du fichier.

    Returns:
        dict: Le dictionnaire lu depuis le fichier.
    """
    async with _get_lock(file):
        return await to_thread(_file_read, file)


def _file_write(data: dict, file: Path) -> None:
    """Écrit un dictionnaire dans un fichier TOML.

    Args:
        data (dict): Le dictionnaire à écrire.
        file (Path): Le chemin du fichier.
    """
    file.write_text(tomlkit.dumps(data))


async def data_write(data: dict, file: Path) -> None:
    """Écrit un dictionnaire dans un fichier TOML, avec un autre thread.

    Args:
        data (dict): Le dictionnaire à écrire.
        file (Path): Le chemin du fichier.
    """
    async with _get_lock(file):
        await to_thread(_file_write, data, file)
