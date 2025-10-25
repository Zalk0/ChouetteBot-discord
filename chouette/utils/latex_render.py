from io import BytesIO

import discord
from aiohttp import ClientSession


# Make a LaTeX rendering function using an online equation renderer : https://latex.codecogs.com/
async def latex_render(session: ClientSession, equation: str) -> discord.File:
    """Rend une équation LaTeX et la renvoie sous forme de fichier.

    Args:
        session (ClientSession): La session HTTP aiohttp.
        equation (str): L'équation LaTeX à rendre.

    Returns:
        discord.File: Le fichier contenant l'image de l'équation rendue.
    """
    options = r"\dpi{200} \bg_black \color[RGB]{240, 240, 240} \pagecolor[RGB]{49, 51, 56}"
    # bg_black is for putting a black background (custom command of the site)
    # instead of the transparent one. Then a custom background color can be used with pagecolor.
    # color is for the text color
    url = f"https://latex.codecogs.com/png.latex?{options} {equation}".replace(" ", "%20")
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
    return await latex_render(session, equation.replace(r" \textrm{}", ""))


async def latex_replace(message: str) -> str:
    """Remplace les caractères spéciaux par des commandes LaTeX.

    Args:
        message (str): Le message à traiter.

    Returns:
        str: Le message avec les caractères remplacés par des commandes LaTeX.
    """
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
        .replace(r"ô", r"\^o")
        .replace(r"Ô", r"\^O")
        .replace(r"û", r"\^u")
        .replace(r"Û", r"\^U")
        .replace(r"ë", r"\"e")
        .replace(r"Ë", r"\"E")
        .replace(r"ü", r"\"u")
        .replace(r"Ü", r"\"U")
        .replace(r"ÿ", r"\"y")
        .replace(r"Ÿ", r"\"Y")
        .replace(r"ñ", r"\~n")
        .replace(r"Ñ", r"\~N")
        .replace(r"¡", r"\!")
        .replace(r"¿", r"\?")
        .replace(r"«", r"\guillemotleft")
        .replace(r"»", r"\guillemotright")
        .replace(r"“", r"\textquotedblleft")
        .replace(r"”", r"\textquotedblright")
        .replace(r"‘", r"\textquoteleft")  # noqa: RUF001
        .replace(r"’", r"\textquoteright")  # noqa: RUF001
        .replace(r"–", r"\textendash")  # noqa: RUF001
        .replace(r"′", r"\textprime")  # noqa: RUF001
        .replace(r"—", r"\textemdash")
        .replace(r"…", r"\ldots")
        .replace(r"‰", r"\textperthousand")
        .replace(r"€", r"\euro")
        .replace(r"£", r"\pounds")
        .replace(r"¢", r"\cent")
        .replace(r"¥", r"\yen")
        .replace(r"§", r"\S")
        .replace(r"¶", r"\P")
        .replace(r"†", r"\dag")
        .replace(r"‡", r"\ddag")
        .replace(r"°", r"\degree")
        .replace(r"µ", r"\micro")
        .replace(r"®", r"\textregistered")
        .replace(r"©", r"\textcopyright")
        .replace(r"™", r"\texttrademark")
        .replace(r"†", r"\textdagger")
        .replace(r"‡", r"\textdaggerdbl")
        .replace(r"•", r"\textbullet")
        .replace(r"·", r"\textperiodcentered")
        .replace(r"…", r"\textellipsis")
        .replace(r"″", r"\textdoubleprime")
        .replace(r"‴", r"\texttripleprime")
        .replace(r"⁗", r"\textquadrupleprime")
        .replace(r"⁰", r"\textsuperscript{0}")
        .replace(r"¹", r"\textsuperscript{1}")
        .replace(r"²", r"\textsuperscript{2}")
        .replace(r"³", r"\textsuperscript{3}")
        .replace(r"⁴", r"\textsuperscript{4}")
        .replace(r"⁵", r"\textsuperscript{5}")
        .replace(r"⁶", r"\textsuperscript{6}")
        .replace(r"⁷", r"\textsuperscript{7}")
        .replace(r"⁸", r"\textsuperscript{8}")
        .replace(r"⁹", r"\textsuperscript{9}")
        .replace(r"₀", r"\textsubscript{0}")
        .replace(r"₁", r"\textsubscript{1}")
        .replace(r"₂", r"\textsubscript{2}")
        .replace(r"₃", r"\textsubscript{3}")
        .replace(r"₄", r"\textsubscript{4}")
        .replace(r"₅", r"\textsubscript{5}")
        .replace(r"₆", r"\textsubscript{6}")
        .replace(r"₇", r"\textsubscript{7}")
        .replace(r"₈", r"\textsubscript{8}")
        .replace(r"₉", r"\textsubscript{9}")
    )
