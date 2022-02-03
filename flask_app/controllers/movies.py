from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models import user
from flask_app.models import movie
import requests

@app.route('/movie_info/<int:movie_id>')
def view_movie_info(movie_id):
    if 'logged_in' not in session:
        return redirect('/')
    film = movie.Movie.get_by_movie_id({ 'movie_id' : movie_id })
    member = user.User.get_by_id({ 'id' : session['member_id'] })
    fans = user.User.get_by_movie_favorited({ 'movie_id' : film.id })
    api_key = "k_kogbi1sw"
    api_call = 'https://imdb-api.com/en/API/Title/' + api_key + '/' + film.imdb_id
    r = requests.get(api_call).json()
    output = {}
    output['title'] = r['title']
    output['id'] = r['id']
    output['image'] = r['image']
    output['year'] = r['year']
    output['releaseDate'] = r['releaseDate']
    output['genres'] = r['genres']
    output['contentRating'] = r['contentRating']
    output['imDbRating'] = r['imDbRating']
    return render_template('movie_view.html', output=output, film=film, member=member, fans=fans)

@app.route('/movies/')
def search_page():
    member = user.User.get_by_id({'id' : session['member_id']})
    return render_template('movie_search.html', member=member)

@app.route('/movies/search/', methods=['POST'])
def search_movie():
    
    search = request.form['search_term']
    
    return redirect('/movies/search/' + search)
    
@app.route('/movies/search/<search_term>')
def show_results(search_term):
    search = search_term
    api_key = "k_kogbi1sw"
    api_call = 'https://imdb-api.com/en/API/Search/' + api_key + '/' + search
    r = requests.get(api_call).json()
    output = []
    print(f'---- {r}')
    for x in r['results']:
        temp_dict = {}
        temp_dict['title'] = x['title']
        temp_dict['id'] = x['id']
        temp_dict['image'] = x['image']
        output.append(temp_dict)
    print(output)
    return render_template('search_results.html', output=output)
    
@app.route('/movies/search/results/', methods=['POST'])
def search_movie_results():
    
    search = request.form['search_select']
    
    return redirect('/movies/search/results/' + search)
    
@app.route('/movies/search/results/<search_term>')
def show_single_result(search_term):
    search = search_term
    api_key = "k_kogbi1sw"
    api_call = 'https://imdb-api.com/en/API/Title/' + api_key + '/' + search
    r = requests.get(api_call).json()
    output = {}
    output['title'] = r['title']
    output['id'] = r['id']
    output['image'] = r['image']
    output['year'] = r['year']
    output['releaseDate'] = r['releaseDate']
    output['genres'] = r['genres']
    output['contentRating'] = r['contentRating']
    output['imDbRating'] = r['imDbRating']
    fave_ids = []
    faves = movie.Movie.get_user_favorites({ 'user_id' : session['member_id']})
    for fave in faves:
        fave_ids.append(fave.imdb_id)
    return render_template('movie_view.html', output=output, fave_ids=fave_ids)

@app.route('/add_favorite/', methods=['POST'])
def add_favorite():
    if 'logged_in' not in session:
        return redirect('/')
    data = {
        'title' : request.form['title'],
        'genre' : request.form['genre'],
        'release_date' : request.form['release_date'],
        'imdb_id' : request.form['imdb_id']
    }
    favorite = movie.Movie.get_by_title(data)
    if not favorite:
        movie.Movie.create(data)
        favorite = movie.Movie.get_by_title(data)
    fav_data = {
        'movie_id' : favorite.id,
        'user_id' : session['member_id']
    }
    user.User.add_favorite(fav_data)
    return redirect('/dashboard')
    