# Tanka

A way to search Last.fm via the terminal

<img width="400" height="260" alt="tanka_demo" src="https://github.com/user-attachments/assets/725a9bb4-5467-4268-a2f3-742ba2dc17d7" />


## Requirements
- Python 3.10+
- A Last.fm API key (create one at [last.fm/api](https://www.last.fm/api)

## Setup
```bash
git clone https://github.com/djmbiana/tanka.git
cd tanka
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration
cp .env.example .env

Then open .env and add your API key:
API_KEY=your_key_here

## Run
``python main.py``

## Usage
- Type an artist name and hit Enter to search
- /quit to exit
- tab to select search bar on results page
