import requests

def get_last_update():
    url = "https://api.github.com/repos/Zalk0/chouettebot-discord/commits/main"

    r = requests.get(url)

    req = r.text.split(":")

    index = 0
    while index < len(req):
        if "date" in req[index]:
            return req[index + 1][1:-3]
            break
        index += 1
