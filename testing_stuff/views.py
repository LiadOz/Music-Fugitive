@app.route('/test', methods=('GET', 'POST'))
def test():
    at = artist_tracker()
    at.append('we are the in crowd')
    at.append('against the current')
    session['at'] = at
    return redirect(url_for('name'))
    form = artist_form()
    if form.validate_on_submit():
        print('noice')
        return 'nice'
    return render_template('test.html', form=form)


@app.route('/test/at')
def name():
    pass
