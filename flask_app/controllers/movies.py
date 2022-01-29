from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models import user
from flask_app.models import movie


@app.route('/movie_info/<int:movie_id>')
def view_movie_info(movie_id):
    if 'logged_in' not in session:
        return redirect('/')
    movie = movie.Movie.get_by_movie_id({ 'movie_id' : movie_id })
    user = user.User.get_by_id({ 'id' : session.id })
    fans = user.User.get_by_movie_favorited({ 'movie_id' : movie_id })
    return render_template('movie_view.html', movie=movie, user=user, fans=fans)

