import asyncio

SPACES = " " * 38


# Check if there is a env var DOCKER_RUNNING and return the status
async def get_running_env() -> bool:
    # Command line to see the DOCKER_RUNNING env variable
    cmd = "echo $DOCKER_RUNNING"

    # Execute the command and read the result
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
    data = await proc.stdout.read()

    # Wait the end of the subprocess
    await proc.wait()

    # Return True if the environnement var is set to true, False otherwise
    if data.decode("ascii").strip() == "true":
        return True
    return False


async def get_image_tag() -> str:
    # Command line to see the IMAGE_TAG env variable
    cmd = "echo $IMAGE_TAG"

    # Execute the command and read the result
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
    data = await proc.stdout.read()

    # Wait the end of the subprocess
    await proc.wait()

    # Return the tag
    return data.decode("ascii").strip()


# Generate the message to log the bot running version
async def get_version() -> str:
    msg = "Version information:\n"

    # Check if the environnement is Docker or not
    if await get_running_env():
        tag = await get_image_tag()
        msg += f"{SPACES}Docker\n{SPACES}Image version: {tag}"

    else:
        # Command line to execute in the shell
        cmd = "git log --format='%D' -n 1;git log --format='%h' -n 1;git log --format='%ci' -n 1"

        # Create the subprocess and redirect the standard output into a pipe
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)

        # Read output lines and store in a variable
        data = await proc.stdout.read()
        info = data.decode("ascii").splitlines()

        # Split the list into specific variables
        branch = info[0].split(",")[0].split("->")[1].strip()
        hash = info[1].strip()
        date = info[2].strip()

        # Wait for the subprocess exit
        await proc.wait()

        # Create message with information and spaces for logs format
        msg += f"{SPACES}Git - {branch}\n{SPACES}Commit hash: {hash}\n{SPACES}Commit date: {date}"
    return msg
