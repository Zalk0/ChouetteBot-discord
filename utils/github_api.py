import aiohttp


# Function to get the last information about main commit with GitHub API
async def get_last_update():
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            "https://api.github.com/repos/Zalk0/chouettebot-discord/commits/main"
        ) as response,
    ):
        commit_infos = await response.json()
    return commit_infos["commit"]["author"]["date"][:10]
