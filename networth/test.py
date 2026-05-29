import requests

uuid = ""
profile_id = ""
api_key = ""
profiles = requests.get(f"https://api.hypixel.net/v2/skyblock/profiles?uuid={uuid}", headers={"API-Key": api_key}).json()
profile = (profile for profile in profiles.get("profiles") if profile.get("profile_id") == profile_id).__next__()
user_profile = profile.get("members").get(uuid)
balance = profile.get("banking").get("balance")
museum = requests.get(f"https://api.hypixel.net/v2/skyblock/museum?profile={profile_id}", headers={"API-Key": api_key}).json()
museum_data = museum.get("members").get(uuid)
networth = requests.post("http://localhost:8080/networth", json={
    "profile": user_profile,
    "museum": museum_data,
    "balance": balance,
})
print(networth.text)
