from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'movies_sn_schema'
    def __init__(self, data):
        self.id = data['id']
        self.screenname = data['screenname']
        self.email = data['email']
        self.password = data['password']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.full_name = f'{self.first_name} {self.last_name}'
        self.city = data['city']
        self.state = data['state']
        self.about_me = data['about_me']
    
    @classmethod
    def create(cls, data):
        query = 'INSERT INTO users (screenname, email, password, first_name, last_name) VALUES ( %(screenname)s, %(email)s, %(password)s, %(first_name)s, %(last_name)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    ### SELECT INDIVIDUAL USERS ###
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])
    
    @classmethod
    def get_by_screenname(cls, data):
        query = 'SELECT * FROM users WHERE screenname = %(screenname)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])
    
    
    ### SELECT MULTIPLE USERS ###
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db_name).query_db(query)
        all_users = []
        if len(results) > 0:
            for row in results:
                all_users.append( cls(row))
        return all_users
    
    @classmethod
    def get_by_movie_favorited(cls, data):
        query = 'SELECT * FROM users JOIN favorites ON users.id = favorites.user_id WHERE favorites.movie_id = %(movie_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query)
        users_favoring = []
        if len(results) > 0:
            for row in results:
                users_favoring.append( cls(row))
        return users_favoring
    
    
    ### DELETE USER ###
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    ### ADD FAVORITE ###
    @classmethod
    def add_favorite(cls, data):
        query = 'INSERT INTO favorites (user_id, movie_id) VALUES ( %(user_id)s, %(movie_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    ### REGISTRATION VALIDATION ###
    @staticmethod
    def validate_registration( form ):
        is_valid = True
        if User.get_by_screenname({'screenname' : form['screenname']}) != None:
            flash('Screenname already registered')
            is_valid = False
        if len(form['screenname']) < 2:
            flash('Screenname must be at least 2 characters')
            is_valid = False
        if User.get_by_email({'email' : form['email']}) != None:
            flash('Email address already registered')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']): 
            flash("Invalid email address")
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must have at least 8 characters')
            is_valid = False
        if form['password'] != form['confirm']:
            flash('Passwords must match')
            is_valid = False
        return is_valid
    
    
    ### PROFILE VALIDATION ###
    #       suggest we avoid validation on the profile update page by not allowing changes to screenname or email