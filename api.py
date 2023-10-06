from flask import session
import json, requests

SPOTIFY_API_URL = "https://api.spotify.com/v1"


# Users API Data Functions
def get_current_users_profile():
    get_current_users_profile_endpoint = f"{SPOTIFY_API_URL}/me"
    get_current_users_profile_response = requests.get(
        get_current_users_profile_endpoint, 
        headers = session["authorization_header"]
    )
    get_current_users_profile_data = json.loads(get_current_users_profile_response.text)
    return get_current_users_profile_data


# Playlists API Data Functions
def get_playlist(playlist_id):
    get_playlist_endpoint = f"{SPOTIFY_API_URL}/playlists/{playlist_id}"
    get_playlist_response = requests.get(
        get_playlist_endpoint,
        headers = session["authorization_header"],
    )
    get_playlist_data = json.loads(get_playlist_response.text)
    return get_playlist_data


def get_playlist_items(playlist_id, limit = 20, offset = 0):
    get_playlist_items_endpoint = \
        f"{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks/?limit={limit}&offset={offset}"
    get_playlist_items_response = requests.get(
        get_playlist_items_endpoint, 
        headers = session["authorization_header"],
    )
    get_playlist_items_data = json.loads(get_playlist_items_response.text)
    playlist_items = []
    for item in get_playlist_items_data["items"]:
        playlist_items.append(item)
    if get_playlist_items_data["next"]:
        return playlist_items + get_playlist_items(playlist_id, offset = limit + offset)
    return playlist_items


def remove_playlist_items(playlist_id, tracks):
    remove_playlist_items_endpoint = f"{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks"
    remove_playlist_items_response = requests.delete(
        remove_playlist_items_endpoint,
        headers = session["authorization_header"],
        data = tracks,
    )
    print(f"remove_playlist_items_response: {remove_playlist_items_response}")


def get_current_users_playlists(limit = 20, offset = 0):
    get_current_users_playlists_endpoint = f"{SPOTIFY_API_URL}/me/playlists/?limit={limit}&offset={offset}"
    get_current_users_playlists_response = requests.get(
        get_current_users_playlists_endpoint, 
        headers = session["authorization_header"]
    )
    get_current_users_playlists_data = json.loads(get_current_users_playlists_response.text)
    current_users_playlists = []
    for item in get_current_users_playlists_data["items"]:
        current_users_playlists.append(item)
    if get_current_users_playlists_data["next"]:
        return current_users_playlists + get_current_users_playlists(offset = limit + offset)
    return current_users_playlists
