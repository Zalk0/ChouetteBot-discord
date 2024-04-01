import aiohttp


async def get_last_update():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.github.com/repos/Zalk0/chouettebot-discord/commits/main"
        ) as response:
            commit_infos = await response.json()
        date = commit_infos["commit"]["author"]["date"][:10]
        return date
