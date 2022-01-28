from flask import Flask, session
import os

app = Flask(__name__)
app.secret_key = 'FLASK_APP_SECRET_KEY'