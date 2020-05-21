# mixes multiple playlists into a new one (need to be authenticated via oauth) 

SCOPE = ''

import credentials
import os
import sys
import spotipy
import spotipy.util as util
import pyperclip
from time import sleep

#prints tracknumber, artist and trackname 
def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

#gets list of user playlists and names of playlists to search
#returns list of ids for given names
def get_playlists(playlists,playlistNames):
    names = []
    if(type(playlistNames) != list):
        names += [playlistNames]
    else:
        names = playlistNames
    playlistIds = []
    for playlistName in names:
        for playlist in playlists['items']:
            if playlist['name'] == playlistName:
                playlistIds.append(playlist['id'])
    return playlistIds

#get playlist tracks providing username, playlist_id and the fields to filter for
def get_playlist_tracks(username,playlist_id,filter):
    results = sp.user_playlist_tracks(username,playlist_id,fields=filter)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


if __name__ == '__main__':
    #get username(s) | possible multiple usernames 
    pyperclip.copy(credentials.credentials.USERNAME)
    usernames=input("Please enter username(s): ").split(',')
    #name of playlistowner
    mainUser=usernames[0]
    #name of playlist
    newPlaylistName=input("Please enter name for new playlist: ")
    #save the id of the playlist after creation
    newPlaylistId = ''
    for i,user in enumerate(usernames):
        print("Authorising user no {0}.".format(i+1))
        token = util.prompt_for_user_token(user,
                                        SCOPE,
                                        credentials.credentials.CLIENT_ID,
                                        credentials.credentials.CLIENT_SECRET,
                                        credentials.credentials.REDIRECT_URI)

        if token:
            sp = spotipy.Spotify(auth=token)
            if i == 0:
                #create the playlist for mainUser and name it playlistName
                sp.user_playlist_create(mainUser,newPlaylistName,public=True)
                playlists=sp.current_user_playlists()
                newPlaylistId = get_playlists(playlists,newPlaylistName)[0]
                if len(newPlaylistId) > 0:
                    #make playlist collaborative
                    sp.user_playlist_change_details(mainUser,newPlaylistId,public=False,collaborative=True)
                else:
                    print('Cant find playlist id')
                    sys.exit()
            #get current user playlists
            playlists = sp.user_playlists(usernames[i])
            #get names of playlists to copy from
            playlistNames = input("Please enter Playlistnames to copy from: ").split(',')
            #get playlist ids
            playlistIds = get_playlists(playlists,playlistNames)

            for id in playlistIds:
                playlistTracks = get_playlist_tracks(usernames[i],id,'items.track.id,next')
                trackList = []
                for track in playlistTracks:
                    trackList.extend([track['track']['id']])
                if len(trackList) > 100:
                    while True:
                        sp.user_playlist_add_tracks(usernames[i],newPlaylistId,trackList[0:100])
                        trackList = trackList[100:len(trackList)]
                        if len(trackList) < 100:
                            sp.user_playlist_add_tracks(usernames[i],newPlaylistId,trackList)
                            break
                else:
                    sp.user_playlist_add_tracks(usernames[i],newPlaylistId,trackList)

        else:
            print("Can't get token for", user)
