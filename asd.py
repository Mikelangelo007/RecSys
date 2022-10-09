import spotipy
from tqdm import tqdm
from spotipy.oauth2 import SpotifyClientCredentials
import os
import json
import pandas as pd
def loop_slices(path, num_slices=20):
  cnt = 0
  mpd_playlists = []
  filenames = os.listdir(path)
  for fname in sorted(filenames):
    print(fname)
    if fname.startswith("mpd.slice.") and fname.endswith(".json"):
      cnt += 1
      fullpath = os.sep.join((path, fname))
      f = open(fullpath)
      js = f.read()
      f.close()
      current_slice = json.loads(js)
      # Create a list of all playlists
      for playlist in current_slice['playlists']:
        mpd_playlists.append(playlist)
      if cnt == num_slices:
        break
  return mpd_playlists
# Path where the json files are extracted
path = 'data/'
playlists = loop_slices(path, num_slices=20)
# Spotify credentials
os.environ["SPOTIPY_CLIENT_ID"] = "e3f2c47591ec485bb73e6e20185404f9"
os.environ["SPOTIPY_CLIENT_SECRET"] = "02b81aca8c764a7984b6960667241d68"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost:8080"
sp = spotipy.Spotify(client_credentials_manager =      
                     SpotifyClientCredentials())
cols_to_keep = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
dfs = []
for playlist in tqdm(playlists):
  audio_feats = []
  for track in playlist['tracks']:
    track_uri = track['track_uri'].split(":")[2]
    feature = sp.audio_features(track_uri)
    if feature:
      audio_feats.append(feature[0])
  avg_feats = pd.DataFrame(audio_feats)[cols_to_keep].mean()
  avg_feats['name'] = playlist['name']
  avg_feats['pid'] = playlist['pid']
  dfs.append(avg_feats.T)
