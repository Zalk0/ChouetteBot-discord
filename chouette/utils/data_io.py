from asyncio import Lock, to_thread
from pathlib import Path

import tomlkit

FILE_LOCKS = {}


def _get_lock(file: Path) -> Lock:
    """Return the lock associated to a path and creates it if it does not exist."""
    for path, lock in FILE_LOCKS.items():
        if path == file:
            return lock
    FILE_LOCKS.update({file: Lock()})
    return FILE_LOCKS.get(file)


def _file_read(file: Path) -> dict:
    try:
        return tomlkit.parse(file.read_text())
    except FileNotFoundError:
        return {}


async def data_read(file: Path) -> dict:
    """In another thread, read a TOML file and returns a dict."""
    async with _get_lock(file):
        return await to_thread(_file_read, file)


def _file_write(data: dict, file: Path) -> None:
    file.write_text(tomlkit.dumps(data))


async def data_write(data: dict, file: Path) -> None:
    """In another thread, write a dict to a TOML file."""
    async with _get_lock(file):
        await to_thread(_file_write, data, file)
