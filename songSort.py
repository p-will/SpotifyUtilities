#Plays songs to user and lets him pick to which playlist the track should be added


import os
import sys
import spotipy
import spotipy.util as util

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

def trackInPlaylists(track,playlists):
    for playlist in playlists:


if __name__ == '__main__':
    username=USERNAME
    token = util.prompt_for_user_token(username,
                                       SCOPE,
                                       CLIENT_ID,
                                       CLIENT_SECRET,
                                       REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        #get users playlists
        playlists = sp.user_playlists(username)
        #filter for playlists where user is owner
        userPlaylists = []
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                userPlaylists.extend([playlist])
        #get users saved tracks
        savedTracks = sp.current_user_saved_tracks()
        #check which tracks aren't part of any playlist yet
        unsortedTracks = []
        while savedTracks['next']:
            for track in savedTracks['items']:


    else:
        print("Can't get token for", username)
