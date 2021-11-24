import json
import pandas as pd
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import requests
import os
from decouple import config


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

input=input("Type in an artist ")

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1'

# Track ID from the URI

# actual GET request with proper header
r = requests.get(BASE_URL+'/search?q='+input+'&type=artist&limit=1', headers=headers)

r = r.json()
id=(r['artists'])
id=(id['items'])
id=id[0]
id=(id['id'])
print(id)

k=requests.get(BASE_URL+'/artists/'+id+'/albums?limit=20',headers=headers)
k=k.json()
print(k)