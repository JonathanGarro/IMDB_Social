import math
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Movie:
    db_name = 'movies_sn_schema'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.genre = data['genre']
        self.release_date = data['release_date']
        self.imdb_id = data['imdb_id']
    
    @classmethod
    def create(cls, data):
        query = 'INSERT INTO movies (title, genre, release_date, imdb_id) VALUES (%(title)s, %(genre)s, %(release_date)s, %(imdb_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    ### SELECT MOVIES ###
    @classmethod
    def get_by_movie_id(cls, data):
        query = 'SELECT * FROM movies WHERE id = %(movie_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])
    
    @classmethod
    def get_by_title(cls, data):
        query = 'SELECT * FROM movies WHERE title = %(title)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_favorites(cls, data):
        query = 'SELECT * FROM movies JOIN favorites ON movies.id = favorites.movie_id WHERE favorites.user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        user_faves = []
        if len(results) == 0:
            return user_faves
        else: 
            for row in results:
                user_faves.append( cls(row))
        return user_faves
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM movies;'
        results = connectToMySQL(cls.db_name).query_db(query)
        all_projects = []
        if len(results) > 0:
            for row in results:
                all_projects.append( cls(row))
        return all_projects
    
    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM movies WHERE id = %(id)s;'
        connectToMySQL(cls.db_name).query_db(query, data)