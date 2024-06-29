import asyncio
from os import getenv

SPACES = " " * 38


async def get_version() -> str:
    """Génère un message avec les informations de version."""
    msg = "Version information:\n"

    # Check if the environnement is Docker or not
    if getenv("DOCKER_RUNNING"):
        tag = getenv("IMAGE_TAG")
        msg += f"{SPACES}Docker\n{SPACES}Image version: {tag}"

    else:
        # Command line to execute in the shell
        cmd = "git log --format='%D' -n 1 && git log --format='%h' -n 1 && git log --format='%ci' -n 1"

        # Create the subprocess and redirect the standard output into a pipe
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)

        # Read output lines and store in a variable
        data = await proc.stdout.read()
        info = data.decode("ascii").splitlines()

        # Split the list into specific variables
        branch = info[0].split(",")[0].split("->")[1].strip()
        commit_hash = info[1].strip()
        date = info[2].strip()

        # Wait for the subprocess exit
        await proc.wait()

        # Create message with information and spaces for logs format
        msg += f"{SPACES}Git - {branch}\n{SPACES}Commit hash: {commit_hash}\n{SPACES}Commit date: {date}"
    return msg
