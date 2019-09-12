from music_fugitive.last import (get_similar, get_artist_songs,
                                 get_artist_genres, get_song_genres,
                                 artist_exists)
from collections import defaultdict
from music_fugitive.util import merge_dicts
from operator import itemgetter


class artist:
    def __init__(self, artist_name):
        self.name = artist_name.lower()
        self.similar = get_similar(artist_name)
        self.top = get_artist_songs(artist_name)


class artist_tracker:
    """
    Class to suggest artists according to other artists or songs.
    self.top_songs contains the 5 top songs of all artists inside.
    """

    SONG_CHANGE_SCORE = 0.3

    def __init__(self):
        self.names = set()
        self.top_songs = {}
        self.scores = defaultdict(int)
        self.similar = {}
        self.genres_scores = defaultdict(int)
        self.blacklist = set()

    def append(self, artist_name):
        """
        Add artist to the liked artists
        """
        if artist_name in self.names:
            return
        new = artist(artist_name)
        self.names.add(new.name.lower())
        self.scores = merge_dicts(lambda x, y: x+y, self.scores, new.similar)

        self.top_songs[artist_name] = new.top
        print(artist_name, new.top)
        self.similar[artist_name] = new.similar
        return

    def artist_exists(self, artist_name):
        """
        Check if artist exists in last fm
        """
        return artist_exists(artist_name)

    def remove(self, artist_name):
        """
        Remove existing artist from liked artists
        """
        if artist_name not in self.names:
            raise Exception('Artist does not exist')
        self.names.remove(artist_name)
        self.top_songs.pop(artist_name)
        self.scores = merge_dicts(lambda x, y: x-y, self.scores,
                                  self.similar[artist_name])
        self.similar.pop(artist_name)

    def update_genres(self, genre, score):
        """
        Update score of specific genre
        """
        print(genre, score)
        self.genres_scores[genre] += score
        return

    def evaluate_songs(self, artist, song, score):
        """
        Changes scores of genres associated with a song
        """
        for tag in get_song_genres(artist, song):
            self.update_genres(tag, score)
        return

    def dislike_artist(self, artist):
        """
        Remove artist from suggestion and lower similar artists scores
        """
        self.blacklist.add(artist)
        similar = get_similar(artist)
        self.scores = merge_dicts(lambda x, y: x-y, self.scores, similar)

    def like_song(self, artist, song):
        self.evaluate_songs(artist, song, self.SONG_CHANGE_SCORE)

    def dislike_song(self, artist, song):
        self.evaluate_songs(artist, song, -self.SONG_CHANGE_SCORE)

    def simple_suggestions(self, count=3):
        """
        Returns a set of suggetions with the count paramater
        which determines how many suggestions from each artist
        will be passed
        """
        result = set()
        for _, artists in self.similar.items():
            for artist in list(artists)[:count]:
                if artist not in self.names:
                    result.add(artist)

        return result

    def get_top(self, entries):
        """
        Returns the top suggested artists
        """
        def calc_score(k, v):
            for tag in get_artist_genres(k):
                v += self.genres_scores[tag]
            return v

        def get_reason(artist):
            similar_to = []
            for similar_artist, sugg in self.similar.items():
                if artist in sugg:
                    similar_to.append(similar_artist)
            return similar_to

        sug = [{'artist': k, 'score': round(calc_score(k, v)),
                'reason': get_reason(k)}
               for k, v in self.scores.items()
               if k not in self.names and k not in self.blacklist]

        print(sug)
        top = tuple(sorted(
            sug, key=itemgetter('score'), reverse=True)[:entries])
        return top
