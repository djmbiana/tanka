from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, Static

import fetcher as fe


class SearchScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(" Sonnet")
        yield Input(placeholder="Search for an artist...")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        artist = event.value
        if artist:
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
            output.append(f" ⌕ {info['name']}")
            output.append(f" Listeners:  {int(info['listeners']):,}")
            output.append(f" Play Count: {int(info['play_count']):,}")
            output.append(f"\n{info['summary']}")

        if tracks:
            output.append("\n ▶ Top Tracks")
            for i, track in enumerate(tracks, start=1):
                output.append(
                    f"  {i}. {track['name']} — {int(track['playcount']):,} plays"
                )

        if similar:
            output.append("\n 𖠋𖠋𖠋 Similar Artists")
            for s in similar:
                output.append(f"  ◦ {s['name']}")

        yield Header()
        yield Static("\n".join(output))
        yield Footer()

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()


class SonnetApp(App):
    def on_mount(self) -> None:
        self.push_screen(SearchScreen())


if __name__ == "__main__":
    app = SonnetApp()
    app.run()
