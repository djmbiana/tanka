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
    try:
        url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={API}&format=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # triggers HTTPError on bad status codes
        parser = response.json()
        if "error" in parser:
            print(f"Error {parser['error']}: {parser['message']}")
            return None

        return {
            "name": parser["artist"]["name"],
            "listeners": parser["artist"]["stats"]["listeners"],
            "play_count": parser["artist"]["stats"]["playcount"],
            "summary": remove_html_tags(parser["artist"]["bio"]["summary"]),
        }
    except requests.exceptions.ConnectionError:
        print("Error: Internet is off")
    except requests.exceptions.Timeout:
        print("Error: Request has timed out")
    except requests.exceptions.TooManyRedirects:
        print("Error: Too many redirects")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {e}")
    except requests.exceptions.JSONDecodeError:
        print("Error: Could not parse response from LastFM")
    except KeyError:
        print("Error: Artist not found")


def fetch_top_tracks(artist):
    try:
        url = f"https://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist}&api_key={API}&format=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # triggers HTTPError on bad status codes
        parser = response.json()
        if "error" in parser:
            print(f"Error {parser['error']}: {parser['message']}")
            return None
        tracks = parser["toptracks"]["track"][:5]
        return [
            {
                "name": track["name"],
                "playcount": track["playcount"],
                "listeners": track["listeners"],
            }
            for track in tracks
        ]
    except requests.exceptions.ConnectionError:
        print("Error: Internet is off")
    except requests.exceptions.Timeout:
        print("Error: Request has timed out")
    except requests.exceptions.TooManyRedirects:
        print("Error: Too many redirects")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {e}")
    except requests.exceptions.JSONDecodeError:
        print("Error: Could not parse response from LastFM")
    except KeyError:
        print("Error: Could not find top tracks")


artist = input("Please search for an artist: ")
info = fetch_artist(artist)
tracks = fetch_top_tracks(artist)
print(" ")
print("=== Artist Info ===")
if info:
    print(info["name"])
    print(info["listeners"])
    print(info["play_count"])
    print(info["summary"])

print(" ")
print("=== Top Tracks ===")
if tracks:
    for i, track in enumerate(tracks, start=1):
        print(
            f"{i}. {track['name']} — {track['playcount']} plays | {track['listeners']} listeners"
        )
