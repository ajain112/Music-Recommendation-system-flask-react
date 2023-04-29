import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

# Authenticate with the Spotify API
client_id = '73642c549e6f42579477ced082e02387'
client_secret = '362e9b8202b44998aacc555d2178390a'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load the CSV file with track IDs
df = pd.read_csv('indian_songs_with_audio_features.csv')
print("Started..........")
# Define a function to fetch the artist name for a given track ID
def get_artist_name(track_id):
    track = sp.track(track_id)
    artist = track['artists'][0]['name']
    return artist

# Apply the function to the track ID column and create a new column for artist name
df['artist_name'] = df['id'].apply(get_artist_name)

print("Saving file")

# Save the updated DataFrame to a new CSV file
df[["id",'artist_name']].to_csv('songs_with_artist.csv', index=False)
