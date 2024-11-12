# twitter_oauth2_client.py

import requests
import base64
import hashlib
import random
import string
from urllib.parse import urlencode
from twitter_config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORIZATION_URL, TOKEN_URL

def generate_code_verifier(length=128):
    """Generate a random string for the code verifier."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_code_challenge(code_verifier):
    """Generate the code challenge using SHA256."""
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(code_challenge).decode().rstrip('=')

def get_authorization_url(code_verifier):
    """Generate the authorization URL."""
    code_challenge = generate_code_challenge(code_verifier)
    
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'tweet.read tweet.write users.read offline.access',  # Add tweet.write
        'state': 'state',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    
    return f"{AUTHORIZATION_URL}?{urlencode(params)}"

def exchange_code_for_token(auth_code, code_verifier):
    """Exchange the authorization code for an access token."""
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to exchange code for token: {response.text}")


def post_tweet(access_token, tweet_text):
    """Post a tweet using the provided access token."""
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "text": tweet_text
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to post tweet: {response.text}")
