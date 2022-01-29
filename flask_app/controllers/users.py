from flask_app import app
from flask import render_template,redirect,session,request, flash, url_for
from flask_app.models import user
from flask_app.models import movie
from flask_bcrypt import Bcrypt
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
def login():
	return render_template('login_reg.html')
	
@app.route('/login/user', methods=['POST'])
def login_process():
	user = user.User.get_user_by_email(request.form)
	
	if not user:
		flash("Invalid Email","login")
		return redirect('/login')
	
	if not bcrypt.check_password_hash(user.password, request.form['password']):
		flash("Invalid Password","login")
		return redirect('/login')
	
	session['member_id'] = user.id
	# flash(f"Welcome, ", "logged_in")
	return redirect('/dashboard')

@app.route('/new/member', methods=['POST'])
def register_user():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        # 'screenname' : request.form['screenname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
        }
    user.User.create(data)
    return redirect('/')