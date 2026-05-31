import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("API_KEY")
artist = input("Search for an artist: ")
url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={API}&format=json"

response = requests.get(url)
parser = response.json()

artist_name = parser["artist"]["name"]
listeners = parser["artist"]["stats"]["listeners"]
play_count = parser["artist"]["stats"]["playcount"]
artist_summary = parser["artist"]["bio"]["summary"]

print(artist_name)
print(listeners)
print(play_count)
print(artist_summary)
