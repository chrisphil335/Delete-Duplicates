from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from api import (
    get_playlist,
    get_current_users_profile,
    get_playlist_items,
    remove_playlist_items,
    get_current_users_playlists,
)
from helpers import (
    playlist_duration,
    track_duration,
)
import json
import random
import requests
import string

# Create App
app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf"

# Client Keys
CLIENT_ID = "aaa0c973b8d94261b33c727edee88e80"
CLIENT_SECRET = "94ebb8f61bba47f8bf326aee13dd1351"

# Spotify URLs
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Authorization Query Parameters
RESPONSE_TYPE = "code"
REDIRECT_URI = "http://127.0.0.1:5000/authorize"
STATE = "".join(random.choices(string.ascii_letters + string.digits, k=16))
SCOPE = "playlist-modify-public playlist-modify-private"
SHOW_DIALOG = "true"

authorization_query_parameters = {
    "client_id": CLIENT_ID,
    "response_type": RESPONSE_TYPE,
    "redirect_uri": REDIRECT_URI,
    "state": STATE,
    "scope": SCOPE,
    "show_dialog": SHOW_DIALOG,
}


# Page Routes
@app.route("/")
def index():
    url_arguments = "&".join([f"{key}={val}" for key, val in authorization_query_parameters.items()])
    authorization_url = f"{SPOTIFY_AUTH_URL}/?{url_arguments}"
    return redirect(authorization_url)


@app.route("/authorize")
def authorize():
    auth_token = request.args["code"]
    code_payload = {
        "grant_type": "authorization_code",
        "code": auth_token,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    session["authorization_header"] = {"Authorization": f"Bearer {access_token}"}
    return redirect(url_for("playlists"))


@app.route("/playlists")
def playlists():
    current_users_playlists = get_current_users_playlists()
    return render_template(
        "playlists.html",
        current_users_playlists = current_users_playlists,
    )


@app.route("/playlist/<playlist_id>")
def playlist(playlist_id):
    current_users_profile = get_current_users_profile()
    playlist = get_playlist(playlist_id)
    playlist_items = get_playlist_items(playlist_id)
    return render_template(
        "playlist.html",
        current_users_profile = current_users_profile,
        playlist = playlist,
        playlist_items = playlist_items,
    )


@app.route("/delete_duplicate_tracks/<playlist_id>")
def delete_duplicate_tracks(playlist_id):
    seen_tracks, duplicate_tracks = [], []
    for i, item in enumerate(get_playlist_items(playlist_id)):
        if item["track"]["uri"] in seen_tracks:
            duplicate_tracks.append({"uri": item["track"]["uri"], "positions": [i]})
        else:
            seen_tracks.append(item["track"]["uri"])
    remove_playlist_items(playlist_id, json.dumps({"tracks": duplicate_tracks}))
    return(redirect(url_for("playlist", playlist_id = playlist_id)))


# Context Processor
@app.context_processor
def context_processor():
    return dict(
        # API Data Functions
        get_playlist = get_playlist,
        get_current_users_profile = get_current_users_profile,
        get_playlist_items = get_playlist_items,
        remove_playlist_items = remove_playlist_items,
        get_current_users_playlists = get_current_users_playlists,

        # Helper Functions
        track_duration = track_duration,
        playlist_duration = playlist_duration,
    )


# Run App
if __name__ == "__main__":
    app.run(debug=True)
