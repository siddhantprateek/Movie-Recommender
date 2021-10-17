from flask import Flask, url_for, render_template, redirect, session
from authlib.integrations.flask_client import OAuth
import requests
import os import environ as env
import sqlite3
import constants
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
app.secret_key = constants.SECRET_KEY


oauth = OAuth(app)
oauth.init_app(app)


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    }
)

@app.route('/')
def index():
    """
    Renders the Home page
    """
    return render_template('index.html')

@app.route('/hello')
def hello():
    email= dict(session).get('email', None)
    return f'hello , {email}'

@app.route('/login')
def login():
    google = oauth.create_client()
    redirect_uri = url_for('authorize', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client()
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/')


@app.route('/user/<name>')
def user(name):
    """
    Renders the user page
    """
    return render_template('user.html', name=name)


@app.route('/subscribe')
def subscribe():
    """
    Renders the subscribe page
    """
    return render_template('subscribe.html')


# @app.route('/github')
# def github():
#     r = requests.get('https://api.github.com/siddhantprateek')
#     return f'{r.json}'


if __name__ == "__main__":
    app.run(debug=True)


# @app.route('/')
# def index():
#     return 'index'
#
#
# @app.route('/login')
# def login():
#     return 'login'
#
#
# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'
#
#
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
