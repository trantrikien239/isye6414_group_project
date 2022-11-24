import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
import pandas as pd
from util_funcs import getTrackFeatures
import time
import json
import sys
import numpy as np

ad_id = '2484350daae248779b1230842ee2c217'
ad_secret = '84a9f644eee1444d8b11b2ed85342dd7'
scope = "user-read-playback-state,user-modify-playback-state,user-library-read,\
user-read-recently-played,user-top-read,user-read-playback-position"
sp = spotipy.Spotify(client_credentials_manager=\
                         SpotifyOAuth(scope=scope,client_id=ad_id, client_secret=ad_secret,\
                                      redirect_uri="http://localhost:8080"))


f=open('sp_avail_funcs.txt','w')
f.write('\n'.join(dir(sp)))
f.close()

ad_curr_track=sp.current_user_recently_played()
curr_tracks=ad_curr_track["items"]

ad_top_tracks=sp.current_user_top_tracks(time_range="long_term", limit=100000)


ad_devices=sp.devices()
sp.start_playback(device_id=ad_devices["devices"][0]["id"],uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])
sp.volume(volume_percent=30)
sp.start_playback(uris=['spotify:track:6GxFgf9cL6e4RcV6h5tMXH'])



tid = 'spotify:track:6gdLoMygLsgktydTQ71b15'

start = time.time()
analysis = sp.audio_analysis(tid)
delta = time.time() - start
print(json.dumps(analysis, indent=4))
print("analysis retrieved in %.2f seconds" % (delta,))



#sp = spotipy.Spotify(auth_manager=client_credentials_manager)


#client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
#sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

scope = "user-read-playback-state,user-modify-playback-state,user-library-read"
sp = spotipy.Spotify(client_credentials_manager=\
                         SpotifyOAuth(scope=scope,clinet_id=ad_id, client_secret=ad_secret))

ad_user_id='31o2xlpfulupjo4ubr4lqu7amvcu'
ad_user=sp.user(ad_user_id)

ad_playlists=sp.user_playlists(user=ad_user_id)
playlist_song_map={}
for i in range(ad_playlists["total"]):
    playlist_i=ad_playlists["items"][i]
    key=(playlist_i["id"],playlist_i["name"])
    # Dataframe to huse features of track in the playlist
    df=pd.DataFrame()
    playlist_song_map[key] = (sp.user_playlist(ad_user_id, key[0]),df)
    track_rows=[]
    for item in playlist_song_map[key][0]['tracks']['items']:
        track = item['track']
        track_id=track['id']
        #Get metadata of track
        track_meta_data=getTrackFeatures(track_id,sp)
        track_rows.append(track_meta_data)
    # create dataset
    df = pd.DataFrame(track_rows,
                      columns=['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability',
                               'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                               'speechiness', 'tempo', 'time_signature'])
    df.to_csv("{}_data.csv".format(key[1]), sep=',')



    df[""]




playlist_ids=[ad_playlists["items"][num_playlist]["id"] for num_playlist in range(ad_playlists["total"])]


def get_tracks_in_playlist(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

ids = get_tracks_in_playlist('angelicadietzel', '4R0BZVh27NUJhHGLNitU08')

ad_playlists=sp.user_playlists(user=ad_user_id)