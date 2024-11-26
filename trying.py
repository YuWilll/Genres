import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

#Change if needed
pool_from = ['pop', 'rock', 'hip-hop', 'edm', 'jazz', 'classical', 
             'country', 'r&b', 'indie', 'blues', 'reggae', 'metal']

songs_per = 10
lim = 50

all_songs = []

#Get audio features from the input track
def grab_features(track_id):
    audio_features = sp.audio_features(track_id)[0]
    return {
        'danceability': audio_features['danceability'],
        'energy': audio_features['energy'],
        'loudness': audio_features['loudness'],
        'speechiness': audio_features['speechiness'],
        'acousticness': audio_features['acousticness'],
        'instrumentalness': audio_features['instrumentalness'],
        'valence': audio_features['valence'],
        'tempo': audio_features['tempo'],
        'key': audio_features['key'],
        'mode': audio_features['mode']
    }

#Get songs by genre
def get_songs(genre, limit, total_songs):
    songs = []
    offset = 0
    while len(songs) < total_songs:
        results = sp.search(q=f'genre:{genre}', type='track', limit=limit, offset=offset)
        tracks = results['tracks']['items']
        for track in tracks:
            song_data = {
                'name': track['name'],
                'artist': ', '.join(artist['name'] for artist in track['artists']),
                'id': track['id'],
                'genre': genre,
                'audio_features' : {}
            }
            songs.append(song_data)
        
        offset += limit
        if len(tracks) < limit:
            break
        time.sleep(1)
          
    return songs

for genre in pool_from:
    print(f"Fetching songs for genre: {genre}")
    genre_songs = get_songs(genre=genre, limit=lim, total_songs=songs_per)
    all_songs.extend(genre_songs)

# Convert to DataFrame
df_songs = pd.DataFrame(all_songs)
print("Done")
# Save to CSV file
#df_songs.to_csv('small_set.csv', index=False)
