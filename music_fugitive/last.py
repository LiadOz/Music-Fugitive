import requests


key = 'e89fd069ab2cbb2a25be2b14cc457674'
api = 'http://ws.audioscrobbler.com/2.0/'

def request_api(params):
    params['api_key'] = key
    params['format'] = 'json'
    res = requests.get(api, params=params).json()
    if 'error' in res:
        print('error \n {}'.format(resp.text))
        return None

    return res


def request_api_list(params, api_param_1, api_param_2, limit=None):
    params['api_key'] = key
    params['format'] = 'json'
    res = requests.get(api, params=params).json()
    if 'error' in res:
        print('error \n{}'.format(resp.text))
        return None

    returned_list = []
    limit_slice = slice(limit)
    for item in res[api_param_1][api_param_2][limit_slice]:
        returned_list.append(item['name'].lower())

    return returned_list


def get_similar(artist):
    """Used to get similar artist to the one inputted
    :param artist: Artist that should be matched
    :return: Dictionary of 10 artists with match value
    """
    params = {'artist': artist, 'method':'artist.getSimilar', 'format':'json', 'limit':10,  'autocorrect':1}
    similar = request_api(params)
    if not similar: return {}

    res = {}
    for artist in similar['similarartists']['artist']:
        res[artist['name'].lower()] = round(float(artist['match']),3)
    return res


def get_artist_songs(artist):
    """Used to get artist best songs
    :param artist: Artist name
    :return: Top 5 songs of the artist
    """
    params = {'artist': artist, 'method': 'artist.getTopTracks', 'limit': 5, 'autocorrect':1}
    return request_api_list(params, 'toptracks', 'track')


def get_artist_genres(artist):
    """
    Returns top 5 tags of artist
    """
    params = {'artist': artist, 'method':'artist.getTopTags', 'autocorrect':1}
    return request_api_list(params, 'toptags', 'tag', limit=5)


def get_song_genres(artist, track):
    """
    Returns top 5 tags of a song
    """
    params = {'track': track, 'artist': artist, 'method': 'track.getTopTags'}
    return request_api_list(params, 'toptags', 'tag', limit=5)


def artist_exists(artist):
    """
    Checks if artist exists in lastfm database
    """
    params = {'artist': artist, 'method':'artist.search', 'limit':1}
    if request_api(params)['results']['artistmatches']['artist']:
        return True
    return False
