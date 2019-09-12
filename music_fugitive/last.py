import requests
import os
from .util import nested_dict_get


key = os.environ.get('LASTFM_KEY')
api = 'http://ws.audioscrobbler.com/2.0/'


def request_api(params, j_location):
    """
    Requests from lastfm using the params
    Returns the nested item inside respose in j_location
    """
    params['api_key'] = key
    params['format'] = 'json'
    res = requests.get(api, params=params).json()
    if 'error' in res:
        print(f"error \n{res['message']}")
        return None

    return nested_dict_get(res, j_location)


def request_api_list(params, j_location, limit=None):
    """
    Requsts the api using params
    Returns a list of items inside j_location
    """
    res = request_api(params, j_location)

    returned_list = []
    for item in res[:limit]:
        returned_list.append(item['name'].lower())

    return returned_list


def get_similar(artist):
    """Used to get similar artist to the one inputted
    :param artist: Artist that should be matched
    :return: Dictionary of 10 artists with match value
    """
    params = {'artist': artist, 'method': 'artist.getSimilar',
              'limit': 10,  'autocorrect': 1}
    similar = request_api(params, j_location=['similarartists', 'artist'])
    if not similar:
        return {}

    res = {}
    for artist in similar:
        res[artist['name'].lower()] = round(float(artist['match']), 3)
    return res


def get_artist_songs(artist):
    """Used to get artist best songs
    :param artist: Artist name
    :return: Top 5 songs of the artist
    """
    params = {'artist': artist, 'method': 'artist.getTopTracks',
              'limit': 5, 'autocorrect': 1}
    return request_api_list(params, j_location=['toptracks', 'track'])


def get_artist_genres(artist):
    """
    Returns top 5 tags of artist
    """
    params = {'artist': artist, 'method': 'artist.getTopTags',
              'autocorrect': 1}
    return request_api_list(params, j_location=['toptags', 'tag'], limit=5)


def get_song_genres(artist, track):
    """
    Returns top 5 tags of a song
    """
    params = {'track': track, 'artist': artist, 'method': 'track.getTopTags'}
    return request_api_list(params, j_location=['toptags', 'tag'], limit=5)


def artist_exists(artist):
    """
    Checks if artist exists in lastfm database
    """
    params = {'artist': artist, 'method': 'artist.search', 'limit': 1}
    if request_api(params, j_location=['results', 'artistmatches', 'artist']):
        return True
    return False
