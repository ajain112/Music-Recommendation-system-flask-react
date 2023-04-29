import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

client_id = client_id
client_secret = client_secret

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, 
    client_secret=client_secret
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Retrieve a list of Indian artists
results = sp.search(q="indian artists", type="artist", limit=1)
artists = results["artists"]["items"]
artist_ids = [artist["id"] for artist in artists]

# Retrieve the top tracks for each artist and extract their audio features
tracks = []
for artist_id in artist_ids:
    top_tracks = sp.artist_top_tracks(artist_id)["tracks"]
    track_ids = [track["id"] for track in top_tracks]
    audio_features = sp.audio_features(track_ids)

    for i, track in enumerate(top_tracks):
        track_features = {}
        if audio_features[i] is not None:
            track_features.update(audio_features[i])
            track_features.update({
                "artist_id": artist_id,
                "artist_name": track["artists"][0]["name"],
                "track_name": track["name"],
                "release_date": track["album"]["release_date"],
                "popularity": track["popularity"],
                "key": track_features["key"],
                "mode": track_features["mode"],
            })
            tracks.append(track_features)


print(df)
time.sleep(1)  # To avoid hitting the rate limit

# Convert the list of tracks to a DataFrame
df_tracks = pd.DataFrame(tracks)

# Group the tracks by artist and calculate the mean audio features
df_artists = df_tracks.groupby(["artist_id", "artist_name"]).agg({
    "acousticness": "mean",
    "danceability": "mean",
    "duration_ms": "mean",
    "energy": "mean",
    "instrumentalness": "mean",
    "liveness": "mean",
    "loudness": "mean",
    "speechiness": "mean",
    "tempo": "mean",
    "valence": "mean",
    "popularity": "mean",
    "key": lambda x: x.value_counts().index[0],
    "mode": lambda x: x.value_counts().index[0],
    "artist_id": "count",
    "genres": lambda x: sp.artist(x.iloc[0])["genres"],
}).reset_index()

# Rename the "artist_id" and "genres" columns
df_artists = df_artists.rename(columns={
    "artist_id": "count",
    "genres": "artist_genres"
})

# Save the DataFrame to a CSV file
df_artists.to_csv("indian_artists_with_audio_features.csv", index=False)

print("Dataset saved to indian_artists_with_audio_features.csv")
