from music_fugitive import app
from flask import render_template, request, redirect, url_for, jsonify, session
from music_fugitive.classes import artist_tracker
from music_fugitive import spotify
from string import capwords
from music_fugitive.forms import artist_form
from functools import wraps


@app.route('/', methods=('GET', 'POST'))
def start():
    form = artist_form()
    if form.validate_on_submit():

        session['sugg'] = artist_tracker()
        for k, v in form.data.items():
            if v and k is not 'csrf_token':
                session['sugg'].append(v)

        return redirect(url_for('question_artists'))

    return render_template('initial_artists.html', form=form)


def initialized(func):
    """
    Checks if the artist_tracker has been initialized with artists.
    Moves user to start otherwise.
    """
    @wraps(func)
    def wrapper(*args):
        if 'sugg' not in session:
            return redirect(url_for('start'))

        return func(*args)

    return wrapper


@app.route('/question_artists')
@initialized
def question_artists():
    artists = [capwords(x) for x in session['sugg'].simple_suggestions(4)]
    data = {'my_list': artists, 'url': '/update_artist',
            'next_endpoint': url_for('question_songs')}
    return render_template('question_artist.html', **data)


@app.route('/update_artist', methods=('GET', 'POST'))
def update_artist():
    subject = request.form['subject'].lower()
    option = request.form['option']

    if option == 'like':
        session['sugg'].append(subject)
    elif option == 'dislike':
        session['sugg'].dislike_artist(subject)
    print(subject, option)
    return jsonify({'result': 'success'})


@app.route('/question_songs')
@initialized
def question_songs():
    def cap_list(songs_list):
        return [capwords(song) for song in songs_list if song]
    songs = [[capwords(artist), cap_list(top)]
             for artist, top in session['sugg'].top_songs.items() if artist]
    print(songs)
    data = {'my_list': songs, 'url': 'update_song',
            'next_endpoint': url_for('top')}
    return render_template('question_song.html', **data)


@app.route('/update_song', methods=('GET', 'POST'))
def update_song():
    artist, song = request.form['subject'].split('_')
    artist = artist.lower()
    song = song.lower()
    option = request.form['option']
    if option == 'like':
        session['sugg'].like_song(artist, song)
    elif option == 'dislike':
        session['sugg'].dislike_song(artist, song)
    print(artist, song, option)
    return jsonify({'result': 'success'})


@app.route('/artist_picture/<artist_name>', methods=['GET'])
def artist_picture(artist_name):
    pic = spotify.get_artist_picture(artist_name)
    if not pic:
        pic = url_for('static', filename='images/artist_not_found.png')
    return jsonify(result=pic)


@app.route('/top')
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
