from textual.app import App, ComposeResult
from textual.containers import Center, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Input, Static

import fetcher as fe

ascii_logo = """
 88888888888     d8888 888b    888 888    d8P         d8888 
     888        d88888 8888b   888 888   d8P         d88888 
     888       d88P888 88888b  888 888  d8P         d88P888 
     888      d88P 888 888Y88b 888 888d88K         d88P 888 
     888     d88P  888 888 Y88b888 8888888b       d88P  888 
     888    d88P   888 888  Y88888 888  Y88b     d88P   888 
     888   d8888888888 888   Y8888 888   Y88b   d8888888888 
     888  d88P     888 888    Y888 888    Y88b d88P     888 
"""


class SearchScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static(ascii_logo, id="title")
        yield Static("search any artist on last.fm\n", id="subtitle")
        with Center():
            yield Input(placeholder="search...", id="search")
        yield Static("\n /quit   exit", id="hint")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        artist = event.value
        if artist == "/quit":
            self.app.exit()
        elif artist:
            self.app.push_screen(ResultsScreen(artist))


class ResultsScreen(Screen):
    def __init__(self, artist: str) -> None:
        super().__init__()
        self.artist = artist

    def compose(self) -> ComposeResult:
        info = fe.fetch_artist(self.artist)
        tracks = fe.fetch_top_tracks(self.artist)
        similar = fe.fetch_similar_artists(self.artist)

        output = []

        if info:
            output.append(f"⌕ {info['name']}")
            output.append(f"Listeners:  {int(info['listeners']):,}")
            output.append(f"Play Count: {int(info['play_count']):,}")
            if info["tags"]:
                output.append(
                    f"\n♫ Genres: {' · '.join(tag.lower() for tag in info['tags'])}"
                )
            output.append("\n✑ Artist Summary:")
            output.append(f"\n{info['summary']}")

        if tracks:
            output.append("\n▶ Top Tracks")
            for i, track in enumerate(tracks, start=1):
                output.append(
                    f"  {i}. {track['name']} — {int(track['playcount']):,} plays"
                )

        if similar:
            output.append("\n𖠋𖠋𖠋 Similar Artists")
            for s in similar:
                output.append(f"  ◦ {s['name']}")

        yield ScrollableContainer(Static("\n".join(output)), id="results")
        with Center():
            yield Input(placeholder="search artist · /quit to exit", id="search")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value == "/quit":
            self.app.exit()
        elif event.value:
            self.app.pop_screen()
            self.app.push_screen(ResultsScreen(event.value))


class TankaApp(App):
    CSS_PATH = "tanka_style.tcss"

    def on_mount(self) -> None:
        self.push_screen(SearchScreen())


if __name__ == "__main__":
    app = TankaApp()
    app.run()
