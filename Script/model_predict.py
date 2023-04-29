import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def predict_song(given_song, tfidf_matrix, new_df, tfidf, cosine_similarity):
    # compute the TF-IDF vector of the given song

    given_song_tfidf = tfidf.transform([given_song])

    # compute the cosine similarity between the TF-IDF vector of the given song and all other TF-IDF vectors
    cosine_similarities = cosine_similarity(given_song_tfidf, tfidf_matrix)[0]

    # get the indices of the sorted cosine similarity scores
    sorted_indices = cosine_similarities.argsort()[::-1]

    # get the titles corresponding to the TF-IDF matrix
    titles = new_df['tag'].values

    li = {}

    # get the 5 most similar songs
    for i,index in enumerate(sorted_indices[0:25]):
        song_dict = new_df[new_df['tag'] == titles[index]][['id', 'name']].to_dict('records')[0]
        li[str(i)] = song_dict
        track_ids = [track['id'] for track in li.values()]
        
    return track_ids

def fetch_image(track_ids):
    client_id = '73642c549e6f42579477ced082e02387'
    client_secret = '362e9b8202b44998aacc555d2178390a'

    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, 
        client_secret=client_secret
    )

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    artist = sp.tracks(track_ids)
    
    return [artist['tracks'][i]['album']['images'][0]['url'] for i in range(len(track_ids))]

