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
            return {"error": parser["message"]}

        return {
            "name": parser["artist"]["name"],
            "listeners": parser["artist"]["stats"]["listeners"],
            "play_count": parser["artist"]["stats"]["playcount"],
            "tags": [tag["name"] for tag in parser["artist"]["tags"]["tag"]],
            "summary": remove_html_tags(parser["artist"]["bio"]["summary"]),
        }
    except requests.exceptions.ConnectionError:
        return {"error": "No internet connection"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.TooManyRedirects:
        return {"error": "Too many redirects"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "Could not parse response from Last.fm"}
    except KeyError:
        return {"error": "Artist not found"}


def fetch_top_tracks(artist):
    try:
        url = f"https://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist}&api_key={API}&format=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # triggers HTTPError on bad status codes
        parser = response.json()
        if "error" in parser:
            return {"error": parser["message"]}
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
        return {"error": "No internet connection"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.TooManyRedirects:
        return {"error": "Too many redirects"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "Could not parse response from Last.fm"}
    except KeyError:
        return {"error": "Artist not found"}


def fetch_similar_artists(artist):
    try:
        url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={API}&format=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # triggers HTTPError on bad status codes
        parser = response.json()
        if "error" in parser:
            return {"error": parser["message"]}
        similar_artists = parser["artist"]["similar"]["artist"][:3]

        return [{"name": similar["name"]} for similar in similar_artists]

    except requests.exceptions.ConnectionError:
        return {"error": "No internet connection"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.TooManyRedirects:
        return {"error": "Too many redirects"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}
    except requests.exceptions.JSONDecodeError:
        return {"error": "Could not parse response from Last.fm"}
    except KeyError:
        return {"error": "Artist not found"}
