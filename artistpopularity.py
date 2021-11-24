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

                                                
# Display and interact with the Window

# Finish up by removing from the screen
