from flask import Blueprint, session, redirect, url_for, render_template
from music_fugitive.classes import artist_tracker
from music_fugitive.forms import artist_form
from string import capwords
from functools import wraps

main = Blueprint('main', __name__)


@main.route('/', methods=('GET', 'POST'))
def start():
    form = artist_form()
    if form.validate_on_submit():

        session['sugg'] = artist_tracker()
        for k, v in form.data.items():
            if v and k is not 'csrf_token':
                session['sugg'].append(v)

        return redirect(url_for('main.question_artists'))

    return render_template('initial_artists.html', form=form)


def initialized(func):
    """
    Checks if the artist_tracker has been initialized with artists.
    Moves user to start otherwise.
    """
    @wraps(func)
    def wrapper(*args):
        if 'sugg' not in session:
            return redirect(url_for('main.start'))

        return func(*args)

    return wrapper


@main.route('/question_artists')
@initialized
def question_artists():
    artists = [capwords(x) for x in session['sugg'].simple_suggestions(4)]
    data = {'my_list': artists, 'url': '/update_artist',
            'next_endpoint': url_for('main.question_songs')}
    return render_template('question_artist.html', **data)


@main.route('/question_songs')
@initialized
def question_songs():
    def cap_list(songs_list):
        return [capwords(song) for song in songs_list if song]
    songs = [[capwords(artist), cap_list(top)]
             for artist, top in session['sugg'].top_songs.items() if artist]
    print(songs)
    data = {'my_list': songs, 'url': 'update_song',
            'next_endpoint': url_for('main.top')}
    return render_template('question_song.html', **data)


@main.route('/top')
@initialized
def top():
    suggestions = session['sugg'].get_top(10)
    for artist in suggestions:
        artist['artist'] = capwords(artist['artist'])
        reason = [capwords(x) for x in artist['reason']]
        if len(reason) == 1:
            artist['reason'] = reason[0]
        else:
            artist['reason'] = ', '.join(reason[:-1]) + ' and ' + reason[-1]
    return render_template('top.html', suggestions=suggestions)
