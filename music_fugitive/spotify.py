import requests
import base64
from time import time
import os
from functools import wraps

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')


class Spot():

    def __init__(self):
        self.token = None
        self.headers = None
        self.expire = 0
        secret = (CLIENT_ID + ':' + CLIENT_SECRET).encode()
        self.authorization = 'Basic ' + base64.b64encode(secret).decode()

    def set_token(self):
        endpoint = 'https://accounts.spotify.com/api/token'
        post = {'grant_type': 'client_credentials'}
        headers = {'Authorization': self.authorization}
        resp = requests.post(endpoint, headers=headers, data=post).json()

        self.token = resp['access_token']
        self.headers = {'Authorization': 'Bearer ' + self.token}
        self.expire = time() + resp['expires_in']

    def valid_token(f):
        """
        Makes sure the token is always valid
        """
        @wraps(f)
        def wrap(self, args):
            if time() > self.expire:
                print('Requsting new token')
                self.set_token()

            return f(self, args)

        return wrap

    @valid_token
    def search_artist(self, artist_name):
        """
        Searched artist spotify id using the artist name
        """
        endpoint = 'https://api.spotify.com/v1/search'
        params = {'q': artist_name, 'type': 'artist', 'limit': 1}
        r = requests.get(endpoint, headers=self.headers, params=params)
        if not r.json()['artists']['items']:
            return ''
        return r.json()['artists']['items'][0]['id']

    @valid_token
    def get_artist_picture(self, artist_name):
        """
        Uses artist Spotify id to find it's image
        """
        artist_id = self.search_artist(artist_name)
        if not artist_id:
            return ''
        endpoint = 'https://api.spotify.com/v1/artists/' + artist_id
        r = requests.get(endpoint, headers=self.headers)
        return r.json()['images'][0]['url']
