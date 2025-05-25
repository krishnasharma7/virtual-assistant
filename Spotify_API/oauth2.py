import requests_oauthlib
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
# Credentials you get from registering a new application
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "https://oauth.pstmn.io/v1/browser-callback"

# OAuth endpoints given in the Spotify API documentation
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
scope = [
     "user-read-email",
     "playlist-read-collaborative",
     "user-modify-playback-state",
     "user-read-currently-playing",
     "app-remote-control",
     "streaming",
     "playlist-modify-public",
     "playlist-read-private",
     "playlist-modify-private",
     "user-read-playback-state",
     "playlist-modify-public",
     "user-follow-modify",
     "user-follow-read",
     "user-read-playback-position",
     "user-top-read",
     "user-read-recently-played",
     "user-library-modify",
     "user-library-read",
     "user-read-private"
 ]

from requests_oauthlib import OAuth2Session
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

# Redirect user to Spotify for authorization
authorization_url, state = spotify.authorization_url(authorization_base_url)
print('Please go here and authorize: ', authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input('\n\nPaste the full redirect URL here: ')

from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth(client_id, client_secret)

# Fetch the access token
token = spotify.fetch_token(token_url, auth=auth,authorization_response=redirect_response)

print(token)

# Fetch a protected resource, i.e. user profile
r = spotify.get('https://api.spotify.com/v1/me')
print(r.content)

