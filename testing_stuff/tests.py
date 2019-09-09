from music_fugitive.classes import artist, artist_tracker
from util import quick_input
from last import get_song_genres
from string import capwords


# at = artist_tracker()
# print('Add favorite artists\n')
# quick_input(at.append)
# print(at.get_top(20))
# print('Here are the top songs of your favorite artists')
# for artist, songs in at.top_songs.items():
#     print()
#     print('Top songs by {}:'.format(capwords(artist)))
#     for song in songs:
#         print(capwords(song))
# 
#     print()
#     print("Type the songs you don't like")
#     quick_input(lambda x: at.evaluate_songs(artist, x, -0.5))
#     print()
#     print('Type the songs you like')
#     quick_input(lambda x: at.evaluate_songs(artist, x, 0.5))
# 
# print(at.genres_scores)
# print(at.get_top(20))
at = artist_tracker()
print('Add favorite artists\n')
quick_input(at.append)
print(at.get_top(20))
print('Choose artists you dont like')
quick_input(at.evaluate_artist)
print(at.blacklist)
print(at.get_top(20))
