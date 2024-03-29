from flask import Flask, session, redirect, request, jsonify, session
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import urllib.parse

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000/callback'

SPOTIFY_AUTH_URL = os.getenv("SPOTIFY_AUTH_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
SPOTIFY_BASE_URL = os.getenv("SPOTIFY_BASE_URL")

class SpotifyAuth:
    def reauthenticate():
        if 'access_token' not in session:
            return redirect('/login')
        
        if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
        
    def login():
        scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private' #change later to create playlist and edit playlist

        params = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'scope': scope,
            'redirect_uri': REDIRECT_URI
        }

        auth_url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"

        return redirect(auth_url)
    
    