from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session
import urllib.parse
import json
from auth import SpotifyAuth

class Amazon:
    auth = SpotifyAuth()

    def reauthenticate(self):
        if not self.auth.accessToken:
            self.auth.login()
        
        if datetime.now().timestamp() > session['expires_at']:
            self.auth.login()