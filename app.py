"""
Random Album Finder Server

A Flask server that serves a static frontend and an API endpoint for
fetching a random album from the MusicBrainz API.

"""

from flask import Flask, jsonify, send_from_directory
import random
import requests

# Flask app setup
app = Flask(__name__, static_folder='static')

MUSICBRAINZ_API = "https://musicbrainz.org/ws/2/release/"

# Fetch a random album
def get_random_album():
    """
    Fetches a random album from the MusicBrainz API and returns its details.

    A random year between 1990 and 2024 is selected to query the MusicBrainz API
    for album releases. If an album is found, it fetches the album's cover image,
    streaming links, and constructs fallback links for popular platforms like Spotify,
    YouTube, and Apple Music.

    Returns:
        dict: A dictionary containing the album's title, artist, cover image URL,
              and a list of streaming links. If no album is found, returns default
              values indicating no data.
    """
    random_year = random.randint(1990, 2024)
    params = {
        "query": f"date:{random_year}",
        "fmt": "json",
        "limit": 1
    }
    response = requests.get(MUSICBRAINZ_API, params=params)
    if response.status_code == 200:
        releases = response.json().get("releases", [])
        if releases:
            album = random.choice(releases)
            cover_url = f"https://coverartarchive.org/release/{album['id']}/front" if "id" in album else None
            
            # Fetch URLs for the album or artist
            listen_links = []
            if "id" in album:
                url_response = requests.get(f"https://musicbrainz.org/ws/2/release/{album['id']}?inc=url-rels&fmt=json")
                if url_response.status_code == 200:
                    relations = url_response.json().get("relations", [])
                    listen_links = [rel["url"]["resource"] for rel in relations if rel["type"] == "streaming"]

            # Fallback links for popular platforms
            fallback_links = [
                f"https://open.spotify.com/search/{album.get('title', '')} {album.get('artist-credit', [{'name': ''}])[0]['name']}",
                f"https://www.youtube.com/results?search_query={album.get('title', '').replace(' ', '+')}+{album.get('artist-credit', [{'name': ''}])[0]['name'].replace(' ', '+')}",
                f"https://music.apple.com/us/search?term={album.get('title', '').replace(' ', '+')}+{album.get('artist-credit', [{'name': ''}])[0]['name'].replace(' ', '+')}"
            ]

            # Combine streaming links and fallback links
            listen_links.extend(fallback_links)
            return {
                "title": album["title"],
                "artist": album.get("artist-credit", [{"name": "Unknown"}])[0]["name"],
                "cover": cover_url or '/static/icons/image.png',
                "links": listen_links
            }
    return {"title": "No data found", "artist": "Unknown", "cover": "/static/icons/image.png", "links": []}

# API route for fetching a random album
@app.route('/api/random_album', methods=['GET'])
def random_album():
    """
    API endpoint to get a random album.

    This endpoint calls the get_random_album function to fetch details
    about a random album from the MusicBrainz API. The album details
    include the title, artist, cover image URL, and streaming links.

    Returns:
        Response: A JSON response containing the album details.
    """
    album = get_random_album()
    return jsonify(album)

# Route to serve the main static frontend page
@app.route('/')
def index():
    """
    Serves the main HTML page of the application.

    This route handles requests to the root URL and sends the index.html
    file located in the static folder as the response, rendering the
    frontend of the application.
    
    Returns:
        Response: The index.html file.
    """
    return send_from_directory(app.static_folder, 'index.html')

# Route to serve other static files such as CSS, JS, etc.
@app.route('/<path:path>')
def static_files(path):
    """
    Serves static files from the static folder.

    This route is used for serving any static files like CSS, JavaScript,
    images, etc., that are requested by the frontend.

    Args:
        path (str): The path of the requested static file.

    Returns:
        Response: The requested static file.
    """
    return send_from_directory(app.static_folder, path)

# Entry point for running the server
if __name__ == '__main__':
    """
    Starts the Flask development server.

    The server listens on host '0.0.0.0' and port 5000, with debugging
    enabled for development purposes. This allows the application to
    be accessed from any IP address on the local network.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)

