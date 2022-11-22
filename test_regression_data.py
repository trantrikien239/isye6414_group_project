#!/usr/bin/env python
# coding: utf-8

# In[1]:


from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint


# In[2]:


client_credentials_manager = SpotifyClientCredentials(client_id="d63bed18ebe04b1ea09d8fb466370112",
    client_secret="83097a8de86940ed81505b3abbb077f5")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# https://newsroom.spotify.com/2021-12-01/what-the-world-streamed-most-in-2021/

# In[3]:


top_5_artists = ["Bad Bunny", "Taylor Swift" "BTS","Drake", "Justin Bieber"]


# In[4]:


search_result={}
for search_str in top_5_artists:
    search_result[search_str] = sp.search(search_str,type="artist",limit=1)
    #pprint(result)


# In[5]:


search_result[search_str].keys()


# In[6]:


search_result[search_str]["artists"]["items"][0]["id"]


# In[7]:


get_artist_id = lambda x: x["artists"]["items"][0]["id"]


# In[9]:


top_ten_tracks_artist = sp.artist_top_tracks("1uNFoZAHBGtllmzznpCI3s")["tracks"]


# In[10]:


top_ten_tracks_artist[0]["id"]


# In[11]:


get_track_id = lambda x: x["id"]


# In[13]:


from util_funcs import *


# In[16]:


import pandas as pd


# In[23]:


pd.DataFrame.from_dict(getTrackFeatures('5PjdY0CKGZdEuoNab3yDmX',sp),orient="index").T


# ### Dummy Pull for 5 artists

# In[43]:


top_artists = ["Bad Bunny", "Taylor Swift", "BTS","Drake", "Justin Bieber",              "Mohit Chauhan", "Amit Trivedi", "Shubh", "AP Dhillon"]


# In[44]:


result = pd.DataFrame()


# In[45]:


for search_str in top_artists:
    print (f"Searching for {search_str}")
    try:
        artist_search = sp.search(search_str,type="artist",limit=1)
        artist_id = get_artist_id(artist_search)
    except:
        print ("-- Error --")
        continue
    top_ten_tracks_artist = sp.artist_top_tracks(artist_id)["tracks"]
    for track in top_ten_tracks_artist:
        track_id = get_track_id(track)
        df_row_track = pd.DataFrame.from_dict(getTrackFeatures(track_id,sp),orient="index").T
        result=result.append(df_row_track)


# In[46]:


result.shape


# In[48]:


result.to_csv("dummy_data.csv")

