import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

# date = input("Please enter date you would like to travel to...in YYYY-MM-DD format\n")
date = "1999-10-11"
URL = "https://www.billboard.com/charts/hot-100/"

response = requests.get(url=URL + date)
code = response.text

soup = BeautifulSoup(code, "html.parser")
lines = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
titles = [item.text for item in lines]
# print(lines)

print(titles)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist on Spotify. Skipped.")