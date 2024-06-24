from asyncio import Lock, to_thread
from pathlib import Path

import tomlkit

FILE_LOCKS = {}


def _get_lock(file: Path) -> Lock:
    """Retourne le verrou associé à un chemin et le crée s'il n'existe pas."""
    for path, lock in FILE_LOCKS.items():
        if path == file:
            return lock
    FILE_LOCKS.update({file: Lock()})
    return FILE_LOCKS.get(file)


def _file_read(file: Path) -> dict:
    """Lit un fichier TOML et retourne un dictionnaire."""
    try:
        return tomlkit.parse(file.read_text())
    except FileNotFoundError:
        return {}


async def data_read(file: Path) -> dict:
    """Dans un autre thread, lit un fichier TOML et retourne un dictionnaire."""
    async with _get_lock(file):
        return await to_thread(_file_read, file)


def _file_write(data: dict, file: Path) -> None:
    """Écrit un dictionnaire dans un fichier TOML."""
    file.write_text(tomlkit.dumps(data))


async def data_write(data: dict, file: Path) -> None:
    """Dans un autre thread, écrit un dictionnaire dans un fichier TOML."""
    async with _get_lock(file):
        await to_thread(_file_write, data, file)
