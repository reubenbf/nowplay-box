import os
import timeago
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler

from datetime import datetime

GH_API = "https://api.github.com"

GIST_ID = os.environ["INPUT_GIST_ID"]
GH_TOKEN = os.environ["INPUT_GH_TOKEN"]

SPOTIPY_USER_ID = os.environ["INPUT_SPOTIPY_USER_ID"]
SPOTIPY_CLIENT_ID = os.environ["INPUT_SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["INPUT_SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["INPUT_SPOTIPY_REDIRECT_URI"]
SPOTIPY_REFRESH_TOKEN = os.environ["INPUT_SPOTIPY_REFRESH_TOKEN"]

scope = 'user-read-currently-playing'

def update_gist(description, content):
	params = {"scope": "gist"}
	headers = {"Authorization": "token {}".format(GH_TOKEN)}
	payload = {"description": description, "public": True, "files": {"Powered by NowPlay-Box!.md": {"content": content}}}

	response = requests.post(GH_API + "/gists/" + GIST_ID, headers=headers, params=params, json=payload)

	if response.status_code == 200 or response.status_code == 201:
		print("Done! The gist was successfully updated!")
	else:
		raise Exception("Error while updating Gist, check your token!")


def main():
	auth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope, open_browser=False, cache_handler=MemoryCacheHandler())
	token = auth.refresh_access_token(SPOTIPY_REFRESH_TOKEN)["access_token"]

	spotify = spotipy.Spotify(auth=token)
	current_track = spotify.current_user_playing_track()

	if not current_track or not current_track.get('item'):
		print("Nothing playing for", SPOTIPY_USER_ID)
		return

	artist = current_track['item']['album']['artists'][0]['name']
	album = current_track['item']['album']['name']
	album_url = current_track['item']['album']['external_urls']['spotify']
	album_img_url = current_track['item']['album']['images'][1]['url']

	created_at = datetime.fromtimestamp(current_track['timestamp']/1000.)
	time_ago = timeago.format(created_at, datetime.now())

	payload = '''# Artist: {} 
## Album: {}
### Check Album Link Below... 


[![]({})]({})
	'''.format(artist,album,album_img_url,album_url)
	update_gist("🎼 Now Playing - {}...".format(time_ago), payload)


if __name__ == "__main__":
	main()
