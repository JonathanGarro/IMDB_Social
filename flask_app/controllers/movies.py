from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models import user
from flask_app.models import movie
import requests

@app.route('/movie_info/<int:movie_id>')
def view_movie_info(movie_id):
    if 'logged_in' not in session:
        return redirect('/')
    movie = movie.Movie.get_by_movie_id({ 'movie_id' : movie_id })
    user = user.User.get_by_id({ 'id' : session.id })
    fans = user.User.get_by_movie_favorited({ 'movie_id' : movie_id })
    return render_template('movie_view.html', movie=movie, user=user, fans=fans)

@app.route('/movies/')
def search_page():
    return render_template('movie_search.html')

@app.route('/movies/search/', methods=['POST'])
def search_movie():
    
    search = request.form['search_term']
    
    return redirect('/movies/search/' + search)
    
@app.route('/movies/search/<search_term>')
def show_results(search_term):
    print(f"SEARCH")
    search = search_term
    api_key = "k_r5saubta"
    api_call = 'https://imdb-api.com/en/API/Search/' + api_key + '/' + search
    r = requests.get(api_call).json()
    output = []
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
    api_key = "k_r5saubta"
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
    print(output)
    return render_template('movie_view.html', output=output)

@app.route('/add_favorite/', methods=['POST'])
def add_favorite():
    if 'logged_in' not in session:
        return redirect('/')
    data = {
        'title' : request.form['title'],
        'genre' : request.form['genre'],
        'release_date' : request.form['release_date']
    }
    favorite = movie.Movie.get_by_title(data)
    if not favorite:
        favorite = movie.Movie.create(data)
    fav_data = {
        'movie_id' : favorite.id,
        'user_id' : session['member_id']
    }
    user.User.add_favorite(fav_data)
    print("running redirect")
    return redirect('/profile_view')
    
@app.route('/profile_view')
def view_profile():
    print("arrived at redirect")
    return render_template('profile_view.html')
        