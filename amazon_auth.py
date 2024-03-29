from flask import Flask, session, redirect, request, jsonify, session
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import urllib.parse

AMAZON_CLIENT_ID = os.getenv("AMAZON_CLIENT_ID")
AMAZON_CLIENT_SECRET = os.getenv("AMAZON_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000/callback'

AMAZON_AUTH_URL = os.getenv("AMAZON_AUTH_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
AMAZON_BASE_URL = os.getenv("AMAZON_BASE_URL")
AMAZON_SESSION = {'accessToken': None, 'expires_at': None}

class AmazonAuth:

    def reauthenticate():
        if 'access_token' not in session:
            return redirect('/login')
        
        if datetime.now().timestamp() > session['expires_at']:
            return redirect('/refresh-token')
        
    def login():
        """scope = 'appstore::apps:readwrite'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data_params = f'grant_type=client_credentials&client_id={AMAZON_CLIENT_ID}&client_secret={AMAZON_CLIENT_SECRET}appstore::apps:readwrite'
        params = {
            "grant_type": "client_credentials",
            'client_id': AMAZON_CLIENT_ID,
            'client_secret': AMAZON_CLIENT_SECRET,
            'scope': scope
        }
        print(f"{AMAZON_AUTH_URL}, headers: {headers}, data: {data_params}")

        #auth_url = f"{AMAZON_AUTH_URL}?{urllib.parse.urlencode(params)}"

        response = requests.post(AMAZON_AUTH_URL, headers=headers, data = data_params)"""
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = f'grant_type=client_credentials&client_id={AMAZON_CLIENT_ID}&client_secret={AMAZON_CLIENT_SECRET}=appstore::apps:readwrite'

        response = requests.post('https://api.amazon.com/auth/O2/token', headers=headers, data=data)
        print(response)
        return 'nothing'
        #AMAZON_SESSION['accessToken'] = response["access_token"]
        #AMAZON_SESSION['expires_at'] = datetime.now().timestamp() + response["expires_in"]

        
    