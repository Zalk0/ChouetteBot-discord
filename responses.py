from src.latex_render import latex_process


async def responses(self, channel, message: str, username: str) -> str:
    # Checks if a message ends with quoi
    if ''.join(filter(str.isalpha, message)).lower().endswith("quoi"):
        return "**FEUR**"

    # Checks if a message contains $$ to signify LaTeX expression
    if message.count("$") > 1:
        if (message.count("$") % 2) == 0:
            await channel.send(file=await latex_process(message))
            self.bot_logger.info(f'{self.user} responded to {username}: "equation.png"')
            return ''
        return "Nombre de $ impair, " \
               "veuillez en mettre un nombre pair pour que je puisse afficher les équations LaTeX !"

    # Return empty string if no condition is checked
    return ''
