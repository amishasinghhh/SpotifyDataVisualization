import PySimpleGUI as sg                        
import json
import pandas as pd
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import requests
from decouple import config
from requests.api import get
from datetime import datetime
import matplotlib.pyplot
import matplotlib.dates



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

program = input("What would you like to see? ")

BASE_URL = 'https://api.spotify.com/v1'


# Define the window's contents
if program == 'album':
    albumlayout = [  [sg.Text("Enter an artist")],     # Part 2 - The Layout
                [sg.Input()],
                [sg.MLine(size=(40,20), key='-OUTPUT-')],
                [sg.Button('Ok')] ]

    # Create the window
    window = sg.Window('Album Average Track Popularity', albumlayout)      # Part 3 - Window Defintion

    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        input=values[0]
        # base URL of all Spotify API endpoints

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

if program=="artistpopularity":
    layout = [  [sg.Text("Enter an artist")],     # Part 2 - The Layout
            [sg.Input()],
            [sg.Text(size=(40,1), key='-OUTPUT-')],
            [sg.Button('Ok')] ]

# Create the window
    window = sg.Window('Artist popularity', layout)      # Part 3 - Window Defintion

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
        gettingArtistPopularity = requests.get(BASE_URL+'/search?q='+input+'&type=artist&limit=1', headers=headers)
        gettingArtistPopularity = gettingArtistPopularity.json()
        popularity=(gettingArtistPopularity['artists'])
        popularity=(popularity['items'])
        popularity=popularity[0]
        popularity=(popularity['popularity'])

        window['-OUTPUT-'].update("Popularity: " + str(popularity))

    window.close()  

if program=="toptracks":
    BASE_URL = 'https://api.spotify.com/v1'

        # Gets ID of an artist from a search
    trackNames = []
    trackPopularities = []
    trackYears = []
    trackMonths = []
    trackDays=[]

    artistinput = input("Which artist do you want to know more about? ")
    gettingArtistID = requests.get(BASE_URL+'/search?q='+artistinput+'&type=artist&limit=1', headers=headers)
    gettingArtistID = gettingArtistID.json()
    id=(gettingArtistID['artists'])
    id=(id['items'])
    id=id[0]
    id=(id['id'])

    # Gets album names and IDs of a particular artist
    gettingTopTracks=requests.get(BASE_URL+'/artists/'+id+'/top-tracks?market=US',headers=headers)
    gettingTopTracks=gettingTopTracks.json()
    topTracks = gettingTopTracks['tracks']
    for i in range(len(topTracks)):
        topTrack = topTracks[i]
        trackNames.append(topTrack['name'])
        trackPopularities.append(topTrack['popularity'])
        gettingTrackRelease = requests.get(BASE_URL+'/tracks/'+topTrack['id']+'?market=ES', headers=headers)
        gettingTrackRelease = gettingTrackRelease.json()
        gettingTrackRelease=gettingTrackRelease['album']
        gettingTrackRelease=gettingTrackRelease['release_date']
        trackYears.append(int(gettingTrackRelease[0:4]))
        trackMonths.append(int(gettingTrackRelease[5:7]))
        trackDays.append(int(gettingTrackRelease[8:]))

    x_values = []
    y_values = []


    for j in range(len(trackYears)):
        x_values.append(datetime(trackYears[j],trackMonths[j],trackDays[j]))
        y_values.append(trackPopularities[j])
    

    dates = matplotlib.dates.date2num(x_values)
    matplotlib.pyplot.plot_date(dates, y_values)  
    plt.ylim([0, 100])
    plt.show()  