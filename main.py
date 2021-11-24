import PySimpleGUI as sg                        
import json
import pandas as pd
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import requests
import os
from decouple import config
from requests.api import get


CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


# Define the window's contents
layout = [  [sg.Text("Enter an artist")],     # Part 2 - The Layout
            [sg.Input()],
            [sg.MLine(size=(40,20), key='-OUTPUT-')],
            [sg.Button('Ok')] ]

# Create the window
window = sg.Window('Window Title', layout)      # Part 3 - Window Defintion

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    input=values[0]
    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1'

    # Track ID from the URI

    # Gets ID of an artist from a search
    gettingArtistID = requests.get(BASE_URL+'/search?q='+input+'&type=artist&limit=1', headers=headers)
    gettingArtistID = gettingArtistID.json()
    id=(gettingArtistID['artists'])
    id=(id['items'])
    id=id[0]
    id=(id['id'])

    # Gets album names and IDs of a particular artist
    gettingAlbums=requests.get(BASE_URL+'/artists/'+id+'/albums?limit=30',headers=headers)
    gettingAlbums=gettingAlbums.json()
    gettingAlbums = (gettingAlbums['items'])
    albumNames=[]
    albumIDs=[]
    i=0
    while i < len(gettingAlbums):
        albumNames.append(gettingAlbums[i]['name'])
        albumIDs.append(gettingAlbums[i]['id'])
        i=i+1

    i=0
    albumTracksPopularity=[]
    toString = ''
    while i<len(albumIDs):
        gettingTracks=requests.get(BASE_URL+'/albums/'+albumIDs[i]+'/tracks', headers=headers)
        gettingTracks=gettingTracks.json()
        gettingTracks=gettingTracks['items']
        j=0
        totalTTrackPopularity=0
        while j<len(gettingTracks):
            trackID=gettingTracks[j]['id']
            gettingTrackPopularity=requests.get(BASE_URL+'/tracks/'+trackID, headers=headers)
            gettingTrackPopularity=gettingTrackPopularity.json()
            gettingTrackPopularity=gettingTrackPopularity['popularity']
            totalTTrackPopularity=totalTTrackPopularity+gettingTrackPopularity
            j=j+1
        albumTracksPopularity.append(totalTTrackPopularity/j)
        toString=toString+str(albumNames[i]) + ": " + str(albumTracksPopularity[i]) + "\n"
        # Output a message to the window
        i=i+1
    # Output a message to the window
    window['-OUTPUT-'].update(toString)

window.close()    