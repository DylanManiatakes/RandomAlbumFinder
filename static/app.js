document.getElementById('random-button').addEventListener('click', () => {
    fetch('/api/random_album')
        .then(response => response.json())
        .then(data => {
            // Update album and artist info
            document.getElementById('album-name').innerText = data.title || "Unknown Album";
            document.getElementById('artist-text').innerText = data.artist || "Unknown Artist";

            // Set album cover as background
            const albumInfo = document.getElementById('album-info');
            if (data.cover) {
                albumInfo.style.backgroundImage = `url('${data.cover}')`;
            } else {
                albumInfo.style.backgroundImage = '';
            }

            // Populate "Where to Listen" links
            const linksList = document.getElementById('links-list');
            linksList.innerHTML = ""; // Clear previous links
            if (data.links && data.links.length > 0) {
                data.links.forEach(link => {
                    const listItem = document.createElement('li');
                    const anchor = document.createElement('a');
                    anchor.href = link;
                    anchor.target = "_blank";
                    anchor.innerText = link;
                    listItem.appendChild(anchor);
                    linksList.appendChild(listItem);
                });
            } else {
                linksList.innerHTML = "<li>No streaming options found.</li>";
            }
        });
});