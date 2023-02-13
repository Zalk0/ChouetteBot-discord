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


# Make a LaTeX process function to use when LaTeX is insertex in a message
async def latex_process(message: str):
    message = await latex_replace(message)
    parts = iter(message.split("$"))
    equation = r'\\'
    try:
        while True:
            word = next(parts)
            if word != '':
                if word.count("\n") > 0:
                    for i in word.split("\n"):
                        if i != '':
                            equation += rf" \textrm{{{i}}}"
                        else:
                            equation += r" \\"
                else:
                    equation += rf" \textrm{{{word}}}"
            word = next(parts)
            if word != '':
                equation += f" {word}"
    except StopIteration:
        pass
    return await latex_render(equation)


# LaTeX replace accents and special characters to commands
async def latex_replace(message: str) -> str:
    message = message.replace(r"ù", r"\`u") \
                     .replace(r"é", r"\'e") \
                     .replace(r"è", r"\`e") \
                     .replace(r"à", r"\`a") \
                     .replace(r"ç", r"\c c") \
                     .replace(r"ê", r"\^e") \
                     .replace(r"ï", r"\"i") \
                     .replace(r"œ", r"\oe") \
                     .replace(r"æ", r"\ae") \
                     .replace(r"î", r"\^i") \
                     .replace(r"À", r"\`A") \
                     .replace(r"É", r"\'E")
    return message
