from io import BytesIO

import discord
import requests


# Make a LaTeX rendering function using an online equation renderer : https://latex.codecogs.com/
# Then send the image as a file
async def latex_render(equation: str) -> discord.File:
    options = r"\bg_black \color[RGB]{240, 240, 240} \pagecolor[RGB]{54, 57, 63}"
    # bg_black is for putting a black background (custom command of the site) instead of a transparent one
    # only then a custom background color can be used with pagecolor. color is for the text color
    url = f"https://latex.codecogs.com/png.latex?\\dpi{{200}} {options} {equation}"
    response = requests.get(url)
    return discord.File(BytesIO(response.content), filename='equation.png')
