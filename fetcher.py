import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()
API = os.getenv("API_KEY")


# This removes the HTML tags present when bio summary is printed
def remove_html_tags(summary):
    return re.sub(r"<.*?>", "", summary).strip()


def fetch_artist(artist):
    url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={API}&format=json"
    response = requests.get(url)
    parser = response.json()

    return {
        "name": parser["artist"]["name"],
        "listeners": parser["artist"]["stats"]["listeners"],
        "play_count": parser["artist"]["stats"]["playcount"],
        "summary": remove_html_tags(parser["artist"]["bio"]["summary"]),
    }


artist = input("Please search for an artist: ")
info = fetch_artist(artist)
print(info["name"])
print(info["listeners"])
print(info["play_count"])
print(info["summary"])
