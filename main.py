import os
import datetime
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://example.com'
billboard_endpoint = 'https://www.billboard.com/charts/hot-100/'
week = ''


def validate_date(date_string):
    """Takes in a date string as input. Validates if date is in the format YYYY-MM-DD. Raises exception if not."""
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def get_billboard_data(date_string):
    """Takes in a date in the format YYYY-MM-DD as input. Identifies the week from the input date.
    Returns a list of song titles in billboard hot 100 for that date."""
    billboard_response = requests.get(f'{billboard_endpoint}{date_string}')
    soup = BeautifulSoup(billboard_response.text, 'html.parser')

    # get the week for the entered date
    global week
    week = soup.find(name='button', class_='date-selector__button')
    week = week.getText().strip('\n').strip('\t').strip()

    # get all song titles
    songs = soup.find_all(name='span', class_='chart-element__information__song')
    song_titles = [song.getText() for song in songs]
    return song_titles


def get_spotify_username():
    """Returns the spotify username of the current user."""
    return sp.current_user()['id']


def get_spotify_song_ids(song_names):
    """Takes in a list of song names as input. Returns a list of corresponding Spotify song IDs."""
    song_ids = []
    for song in song_names:
        song_data = sp.search(q=f"track:{song} year:{date.split('-')[0]}", type='track', limit=1)
        try:
            song_id = song_data['tracks']['items'][0]['id']
        except IndexError:
            print(f'Song "{song}" not found on Spotify. Skipped it.')
        else:
            song_ids.append(song_id)
    return song_ids


def create_spotify_playlist(song_ids):
    """Takes in a list of song IDs as input. Creates a new Spotify playlist adding all songs in the list. Returns the link to the playlist."""
    create_playlist_response = sp.user_playlist_create(user=get_spotify_username(),
                                                       name=f'Billboard Hot 100: {week}',
                                                       description=f'A playlist consisting of all songs from Billboard Hot 100 list for the week of {week}',
                                                       public=True)
    sp.playlist_add_items(playlist_id=create_playlist_response['id'], items=song_ids)
    return create_playlist_response['external_urls']['spotify']


# Authenticate with spotify using spotipy library
spotify_scope = 'playlist-modify-public playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=spotify_scope,
                                               show_dialog=True,
                                               client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI))

date = input('Which date do you want to travel to? (Enter the date in YYYY-MM-DD format) : ')
validate_date(date)
billboard_song_names = get_billboard_data(date)
spotify_song_ids = get_spotify_song_ids(song_names=billboard_song_names)
spotify_playlist_link = create_spotify_playlist(song_ids=spotify_song_ids)
print(f'\nSuccessfully created playlist: {spotify_playlist_link}')
