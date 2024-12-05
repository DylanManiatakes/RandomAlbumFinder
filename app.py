from flask import Flask, jsonify, send_from_directory
import random
import requests

# Flask app setup
app = Flask(__name__, static_folder='static')

MUSICBRAINZ_API = "https://musicbrainz.org/ws/2/release/"

# Fetch a random album
def get_random_album():
    random_year = random.randint(1960, 2022)
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
                "cover": cover_url or '/static/placeholder.jpg',
                "links": listen_links
            }
    return {"title": "No data found", "artist": "Unknown", "cover": "/static/placeholder.jpg", "links": []}

# API route for random album
@app.route('/api/random_album', methods=['GET'])
def random_album():
    album = get_random_album()
    return jsonify(album)

# Route to serve the static frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (CSS, JS, etc.)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)