import requests
import base64
from time import time

client_id = '0995c419e0b94ba6a828cdd763aec133'
client_secret = '3de7339b9b2642bebf8b1b5d75de17a8'

token = None
headers = None
expire = 0

def set_token():
    global expire
    global token
    global headers
    endpoint = 'https://accounts.spotify.com/api/token'
    secret = client_id + ':' + client_secret
    authorization = 'Basic ' + base64.b64encode(secret.encode()).decode()
    post = {'grant_type': 'client_credentials'}
    headers = {'Authorization': authorization}
    r = requests.post(endpoint, headers=headers, data=post)
    resp = r.json()

    expire = time() + resp['expires_in']
    token = resp['access_token']
    headers = {'Authorization': 'Bearer ' + token}
    return


def valid_token(f):
    def wrapper(args):
        if time() > expire:
            print('Requsting new token')
            set_token()

        return f(args)

    return wrapper


@valid_token
def search_artist(artist_name):
    endpoint = 'https://api.spotify.com/v1/search'
    params = {'q': artist_name, 'type': 'artist', 'limit':1}
    r = requests.get(endpoint, headers=headers, params=params)
    if not r.json()['artists']['items']:
        return ''
    return r.json()['artists']['items'][0]['id']


@valid_token
def get_artist_picture(artist_name):
    artist_id = search_artist(artist_name)
    if not artist_id:
        return ''
    endpoint = 'https://api.spotify.com/v1/artists/' + artist_id
    r = requests.get(endpoint , headers=headers)
    return r.json()['images'][0]['url']


g = get_artist_picture
from pprint import pprint as p
