from flask_app import app
from flask import render_template,redirect,session,request, flash, url_for
from flask_app.models import user
from flask_app.models import movie
from flask_bcrypt import Bcrypt
import requests
bcrypt = Bcrypt(app)

@app.route('/index')
@app.route('/')
def index():
	# clear out the session cache to avoid member data issues on-load
	session.clear()
	return render_template('index.html')
	
@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/login')
def load_login_and_reg():
	return render_template('login_reg.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/login/member', methods=['POST'])
def user_login():
	member = user.User.get_by_email(request.form)
	
	if not member:
		flash("Invalid Email","login")
		return redirect('/login')
	
	if not bcrypt.check_password_hash(member.password, request.form['password']):
		flash("Invalid Password","login")
		return redirect('/login')
	
	session['member_id'] = member.id
	session['user_email'] = member.email
	session['logged_in'] = True
	# flash(f"Welcome, ", "logged_in")
	return redirect('/dashboard')

@app.route('/new/member', methods=['POST'])
def register_user():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'screenname' : request.form['screenname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
        }
    user.User.create(data)
    return redirect('/dashboard')

@app.route('/update/member', methods=['POST'])
def update_user():
    if 'user_id' not in session:
        return redirect('/logout')
    if user.User.edit_user(request.form):
        return redirect(f"/update/member/{request.form['id']}")
    # if not user.User.validate_registration(request.form):
    #     return redirect('/')
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'screenname' : request.form['screenname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
        }
    user.User.create(data)
    return redirect('/profile_view')

@app.route('/profile_view')
def view_profile():
    member = user.User.get_by_id({'id' : session['member_id']})
    print("arrived at redirect")
    return render_template('profile_view.html', member=member )

#route for other users profiles
#Routing needs to be fixed
@app.route('/profile_view/<member_id>')
def view_user_profile(member_id):
    member = user.User.get_by_id({'id' : member_id})
    return render_template('user_profile.html', member=member)


@app.route('/profile_edit')
def view_profile_edit():
    member = user.User.get_by_id({'id': session['member_id']})
    return render_template('profile_edit.html',member=member)
    

@app.route('/dashboard')
def load_dashboard():
    if 'logged_in' not in session:
        return redirect('/')
    member = user.User.get_by_id({'id' : session['member_id']})
    user_faves = movie.Movie.get_user_favorites({'user_id' : session['member_id']})
    faves_ids = [x.imdb_id for x in user_faves]
    movies = movie.Movie.get_all()
    output =[]
    api_key = "k_kogbi1sw"
    for favorite in user_faves:
        api_call = 'https://imdb-api.com/en/API/Title/' + api_key + '/' + favorite.imdb_id
        r = requests.get(api_call).json()
        output.append(r)
    print(output)
    return render_template('dashboard.html', member=member, output=output, user_faves=user_faves, movies=movies, faves_ids=faves_ids)
