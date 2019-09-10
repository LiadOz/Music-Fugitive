from flask import Blueprint, request, session, jsonify, url_for
from music_fugitive import spotify

post = Blueprint('post', __name__)


@post.route('/update_artist', methods=('GET', 'POST'))
def update_artist():
    subject = request.form['subject'].lower()
    option = request.form['option']

    if option == 'like':
        session['sugg'].append(subject)
    elif option == 'dislike':
        session['sugg'].dislike_artist(subject)
    print(subject, option)
    return jsonify({'result': 'success'})


@post.route('/update_song', methods=('GET', 'POST'))
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


@post.route('/artist_picture/<artist_name>', methods=['GET'])
def artist_picture(artist_name):
    pic = spotify.get_artist_picture(artist_name)
    if not pic:
        pic = url_for('static', filename='images/artist_not_found.png')
    return jsonify(result=pic)
