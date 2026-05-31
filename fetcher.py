import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("API_KEY")
artist = "The Cure"

url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={API}&format=json"

response = requests.get(url)

