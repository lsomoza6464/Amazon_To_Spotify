from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session
import urllib.parse
import json
from auth import SpotifyAuth

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

REDIRECT_URI = os.getenv('REDIRECT_URI')

SPOTIFY_AUTH_URL = os.getenv("SPOTIFY_AUTH_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
SPOTIFY_BASE_URL = os.getenv("SPOTIFY_BASE_URL")

class Spotify:
    auth = SpotifyAuth()

    def reauthenticate(self):
        if 'access_token' not in session:
            return redirect('/login')
        
        if datetime.now().timestamp() > session['expires_at']:
            print('here')
            self.refresh_token()
        
    def refresh_token(self):
        print("refresh token")
        if 'refresh_token' not in session:
            self.auth.login
        
    
        
    def get_header(self):
        headers = {
            'Authorization': f"Bearer {session['access_token']}"
        }
        return headers

    def get_header_content_type(self):
        headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {session['access_token']}"
        }
        return headers

    def get_user_id(self):
        self.reauthenticate()

        response = requests.get(SPOTIFY_BASE_URL + 'me', headers = self.get_header())
        user_info = response.json()
        user_id = user_info['id']
        return user_id

    def get_playlists(self):
        self.reauthenticate()

        response = requests.get(SPOTIFY_BASE_URL + 'me/playlists', headers=self.get_header())
        playlists = response.json()
        return jsonify(playlists)

    def copy_playlist(self):
        curr_playlist_id = self.create_playlist()
        self.populate_playlist(curr_playlist_id)
        return redirect('/get-playlists')

    def create_playlist(self):
        self.reauthenticate()

        req_body = json.dumps({
            'name': 'Logan playlist',
            'description': 'first playlist',
            'public': True
        })
        #print(f'requestStuff: {SPOTIFY_BASE_URL}users/{get_user_id()}/playlists')
        response = requests.post(f'{SPOTIFY_BASE_URL}users/{self.get_user_id()}/playlists', data=req_body, headers=self.get_header_content_type())
        return response.json()['id']

    def get_track_id(self, artist, song, album = ''):
        searchInput = f'{artist} {album} {song}'

        response = requests.get(f'{SPOTIFY_BASE_URL}search?q={searchInput}&type=track&limit=1', headers=self.get_header())
        responseJSON = response.json()
        song_name = responseJSON['tracks']['items'][0]['name']
        track_id_uri = responseJSON['tracks']['items'][0]['uri']
        print(song_name + ': ' + track_id_uri)
        return track_id_uri

    def populate_playlist(self, playlist_id):
        self.reauthenticate()
        track_id1 = self.get_track_id('Joji', '777', 'Nectar')
        track_id2 = self.get_track_id('Joji', 'Daylight')
        req_body = json.dumps({
            'uris': [track_id1, track_id2]
        })
        url = f'{SPOTIFY_BASE_URL}playlists/{playlist_id}/tracks'
        print(url)
        requests.post(url, headers=self.get_header_content_type(), data=req_body)
        #maybe dont need response


