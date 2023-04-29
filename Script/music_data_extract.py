import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

client_id = client_id
client_secret = client_secret

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, 
    client_secret=client_secret
)

for j in range(1):
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # Create a CSV file and write the header row
    with open("indian_songs_with_audio_features.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if j == 0:
            writer.writerow([
                "id", "name", "artist",'artist_id', "album", "release_date", "popularity", "duration_ms", 
                "acousticness", "danceability", "energy", "instrumentalness", "key",
                "liveness", "loudness", "mode", "speechiness", "tempo", "time_signature",
                "track_href", "uri", "valence"
            ])
        if True:
            offset = 1000
            limit = 50
            query = "indian song"
            total_tracks = 0
            for i in range(20):
                print(f"Retrieved 50 tracks (total: {50*(i+1)})")
                results = sp.search(q = query, type="track", limit=limit, offset=offset)
                tracks = results["tracks"]["items"]
                if not tracks:
                    break

                track_ids = [track["id"] for track in tracks]
                audio_features = sp.audio_features(track_ids)

                for i, track in enumerate(tracks):
                    try:
                        row = [
                            track["id"],
                            track["name"],
                            [track["artists"][i]['name'] for i in range(len(track["artists"]))],
                            [track["artists"][i]['id'] for i in range(len(track["artists"]))] ,
                            track["album"]["name"],
                            track["album"]["release_date"],
                            track["popularity"],
                            track["duration_ms"],
                            audio_features[i]["acousticness"],
                            audio_features[i]["danceability"],
                            audio_features[i]["energy"],
                            audio_features[i]["instrumentalness"],
                            audio_features[i]["key"],
                            audio_features[i]["liveness"],
                            audio_features[i]["loudness"],
                            audio_features[i]["mode"],
                            audio_features[i]["speechiness"],
                            audio_features[i]["tempo"],
                            audio_features[i]["time_signature"],
                            track["href"],
                            track["uri"],
                            audio_features[i]["valence"]
                        ]
                        writer.writerow(row)
                        # print(track["artists"][0]['id'])
                    except Exception as e:
                        pass
                total_tracks += len(tracks)
                offset += limit
                time.sleep(1)  # To avoid hitting the rate limit

                if total_tracks >= 100000:
                    break

print("Dataset saved to indian_songs_with_audio_features.csv")
