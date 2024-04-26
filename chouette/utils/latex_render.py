from io import BytesIO

import aiohttp
import discord


# Make a LaTeX rendering function using an online equation renderer : https://latex.codecogs.com/
# Then send the image as a file
async def latex_render(equation: str) -> discord.File:
    options = r"\dpi{200} \bg_black \color[RGB]{240, 240, 240} \pagecolor[RGB]{49, 51, 56}"
    # bg_black is for putting a black background (custom command of the site)
    # instead of the transparent one. Then a custom background color can be used with pagecolor.
    # color is for the text color
    url = f"https://latex.codecogs.com/png.latex?{options} {equation}".replace(" ", "%20")
    async with aiohttp.ClientSession() as session, session.get(url) as response:
        response_content = await response.read()
    return discord.File(BytesIO(response_content), filename="equation.png")


# Make a LaTeX process function to use when LaTeX maths is inserted in a message
async def latex_process(message: str):
    message = await latex_replace(message)
    parts = message.split("$")
    equation = r"\\"
    for i in range(len(parts)):
        if i != "":
            if i % 2:  # It's maths, so nothing to do
                equation += f" {parts[i]}"
            else:  # It's text
                if parts[i].count("\n") > 0:
                    linebreak = r"} \\ \textrm{".join(parts[i].split("\n"))
                    # Not using splitlines method
                    # Because I need to keep linebreaks at the end of the text
                    equation += rf" \textrm{{{linebreak}}}"
                else:
                    equation += rf" \textrm{{{parts[i]}}}"
    return await latex_render(equation.replace(r" \textrm{}", ""))


# LaTeX replace accents and special characters to commands
# TODO: Add all the symbols that may appear
async def latex_replace(message: str) -> str:
    return (
        message.replace(r"ù", r"\`u")
        .replace(r"é", r"\'e")
        .replace(r"è", r"\`e")
        .replace(r"ê", r"\^e")
        .replace(r"à", r"\`a")
        .replace(r"ï", r"\"i")
        .replace(r"î", r"\^i")
        .replace(r"œ", r"\oe")
        .replace(r"æ", r"\ae")
        .replace(r"Ï", r"\¨I")
        .replace(r"Î", r"\^I")
        .replace(r"À", r"\`A")
        .replace(r"É", r"\'E")
        .replace(r"È", r"\`E")
        .replace(r"Ê", r"\^E")
        .replace(r"ç", r"\c c")
        .replace(r"Ç", r"\c C")
    )
