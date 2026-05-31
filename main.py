import fetcher as fe

artist = input("Please search for an artist: ")
info = fe.fetch_artist(artist)
tracks = fe.fetch_top_tracks(artist)
similar_artists = fe.fetch_similar_artists(artist)
print(" ")
print("=== Artist Info ===")
if info:
    print(info["name"])
    print(f"Listners: {int(info['listeners']):,}")
    print(f"Play Count: {int(info['play_count']):,}")
    print(info["summary"])

print(" ")
print("=== Top Tracks ===")
if tracks:
    for i, track in enumerate(tracks, start=1):
        print(
            f"{i}. {track['name']} - {int(track['playcount']):,} plays | {int(track['listeners']):,} listeners"
        )
print(" ")
print("=== Similar Artists ===")
if similar_artists:
    for i, similar in enumerate(similar_artists, start=1):
        print(f"◦ {similar['name']}")
