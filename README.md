
# Random Album Finder 🎵

Discover random music albums with streaming links and a sleek, modern interface! This app fetches album data from MusicBrainz, provides fallback links to Spotify, YouTube, and Apple Music, and is built as a Progressive Web App (PWA) for easy access on any device.

![App Preview](static/icons/icon-512x512.png)

## Features
- Fetch random albums and artist details.
- Get links to listen on popular platforms.
- Progressive Web App (PWA) for offline access.
- Dockerized for easy deployment.

---

## 🚀 Deployment

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/RandomAlbumFinder.git
   cd RandomAlbumFinder
   ```

2. Install dependencies:
   ```bash
   pip install flask requests
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

### Deploy with Docker
1. Build the Docker image:
   ```bash
   docker build -t random-album-finder .
   ```

2. Run the container:
   ```bash
   docker run -d -p 5000:5000 random-album-finder
   ```

3. Access the app at:
   ```
   http://<your-server-ip>:5000
   ```

---

## 🌟 Progressive Web App (PWA)

- Install the app on your device:
  1. Open the app in a modern browser (e.g., Chrome, Edge).
  2. Click the "Install" or "Add to Home Screen" option.

---

## 🛠 Project Structure

```
RandomAlbumFinder/
├── app.py                 # Main Flask app
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── static/
│   ├── styles.css         # App styling
│   ├── app.js             # Frontend logic
│   ├── manifest.json      # PWA manifest
│   ├── service-worker.js  # Service worker for PWA
│   └── icons/             # PWA icons
└── README.md              # Project documentation
```

---

## 🌐 APIs Used
- [MusicBrainz](https://musicbrainz.org): Fetches random album and artist details.
- Fallback links for Spotify, YouTube, and Apple Music.

---

## ✨ Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue.

---

## 📝 License
This project is open source under the [MIT License](LICENSE).
