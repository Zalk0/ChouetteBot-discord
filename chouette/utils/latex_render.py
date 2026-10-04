from io import BytesIO

import discord
from aiohttp import ClientSession


# Make a LaTeX rendering function using an online equation renderer : https://fxtex.codecogs.com
async def latex_render(session: ClientSession, equation: str) -> discord.File:
    """Rend une équation LaTeX et la renvoie sous forme de fichier.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        equation (str): L'équation LaTeX à rendre.

    Returns:
        discord.File: Le fichier contenant l'image de l'équation rendue.
    """
    options = r"\dpi{200} \fg{f0f0f0} \bg{313338}"
    # fg is for the text color.
    # bg is for the background color.
    url = url_encode(f"https://fxtex.codecogs.com/png.image?{options} {equation}")
    async with session.get(url) as response:
        response_content = await response.read()
    return discord.File(BytesIO(response_content), filename="equation.png")


async def latex_process(session: ClientSession, message: str) -> discord.File:
    """Rend un message contenant des équations LaTeX et le renvoie sous forme de fichier.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        message (str): Le message à traiter.

    Returns:
        discord.File: Le fichier contenant l'image de l'équation rendue.
    """
    parts = message.split("$")
    equation = r"\\"
    for i in range(len(parts)):
        if parts[i] != "":
            if i % 2:  # It's maths, so nothing to do
                equation += f" {parts[i]}"
            # It's text
            elif parts[i].count("\n") > 0:
                linebreak = r"} \\ \textrm{".join(parts[i].split("\n"))
                # Not using splitlines method
                # Because I need to keep linebreaks at the end of the text
                equation += rf" \textrm{{{linebreak}}}"
            else:
                equation += rf" \textrm{{{parts[i]}}}"
    return await latex_render(session, equation.replace(r" \textrm{}", ""))


def url_encode(message: str) -> str:
    """Encode les caractères spéciaux en forme %.

    Args:
        message (str): Le message à traiter.

    Returns:
        str: Le message avec les caractères remplacés par l'encodage URL.
    """
    return message.replace(" ", "%20").replace("+", "%2B").replace("&", "%26").replace("#", "%23")
