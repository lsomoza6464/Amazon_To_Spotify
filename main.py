from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session
import urllib.parse
import json
from auth import SpotifyAuth
from amazon_auth import AmazonAuth
from spotify import Spotify

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

REDIRECT_URI = os.getenv('REDIRECT_URI')

SPOTIFY_AUTH_URL = os.getenv("SPOTIFY_AUTH_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
SPOTIFY_BASE_URL = os.getenv("SPOTIFY_BASE_URL")

spotify = Spotify()
auth = spotify.auth

@app.route('/')
def index():
    #return index
    #return "Welcome to my Amazon App <a href='/amazonLogin'>Login with Amazon</a>"
    return "Welcome to my Spotify App <a href='/spotifyLogin'>Login with Spotify</a>"

def amazon_login():
    AmazonAuth.login


app.add_url_rule('/spotifyLogin', 'login', SpotifyAuth.login)

app.add_url_rule('/amazonLogin', 'amazonLogin', AmazonAuth.login)



@app.route('/callback')
def callback():
    if 'error' in request.args: #error case
        return jsonify({"error": request.args['error']})
    
    if 'code' in request.args: #successful
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/create-populate-playlist')

@app.route('/create-populate-playlist')
def createPopulatePlaylist():
    playlistId = spotify.create_playlist()
    spotify.populate_playlist(playlistId)

    return spotify.get_playlists()
    
@app.route('/refresh-token')
def refresh_token():
    print("refresh token")
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        
        return redirect('/playlists')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)