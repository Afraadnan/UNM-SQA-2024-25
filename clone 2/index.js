const videoGrid = document.getElementById('video-grid');
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const keywordButtons = document.querySelectorAll('.keyword-btn');
const newKeywordInput = document.getElementById('newKeyword');
const addKeywordButton = document.getElementById('addKeywordButton');
const keywordContainer = document.querySelector('.keywords');
const sortOptions = document.getElementById('sortOptions');

// YouTube API key
const API_KEY = 'AIzaSyDN-T0QfzzQtTABG9xbBjNpPjd1JDL1XE0';
const SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search';
const VIDEO_URL = 'https://www.googleapis.com/youtube/v3/videos';

// Function to fetch videos with caching
const fetchVideos = async (query, sortBy = '') => {
    // Check if the data is already cached
    const cacheKey = `${query}-${sortBy}`;
    const cachedData = localStorage.getItem(cacheKey);

    if (cachedData) {
        displayVideos(JSON.parse(cachedData));
        return;
    }

    try {
        // Fetch video IDs from search endpoint
        const searchResponse = await fetch(
            `${SEARCH_URL}?part=snippet&type=video&maxResults=12&q=${query}&key=${API_KEY}`
        );
        const searchData = await searchResponse.json();

        if (!searchData.items || searchData.items.length === 0) {
            videoGrid.innerHTML = '<p>No videos found. Please try a different query.</p>';
            return;
        }

        // Extract video IDs
        const videoIds = searchData.items.map((video) => video.id.videoId).join(',');

        // Fetch video details from videos endpoint
        const videoResponse = await fetch(
            `${VIDEO_URL}?part=snippet,contentDetails&maxResults=15&id=${videoIds}&key=${API_KEY}`
        );
        const videoData = await videoResponse.json();

        // Map video details
        const videos = videoData.items.map((video) => ({
            id: video.id,
            title: video.snippet.title,
            publishedAt: new Date(video.snippet.publishedAt), // Convert to Date
            duration: parseISO8601Duration(video.contentDetails.duration), // Convert to seconds
            thumbnail: video.snippet.thumbnails.high.url,
        }));

        // Apply sorting
        let sortedVideos = videos;
        if (sortBy === 'duration') {
            sortedVideos = videos.sort((a, b) => a.duration - b.duration); // Shortest to longest
        } else if (sortBy === 'age') {
            sortedVideos = videos.sort((a, b) => b.publishedAt - a.publishedAt); // Newest to oldest
        }

        // Cache the videos for later use
        localStorage.setItem(cacheKey, JSON.stringify(sortedVideos));

        displayVideos(sortedVideos);
    } catch (error) {
        console.error('Error fetching videos:', error);

        if (error.response && error.response.status === 403) {
            videoGrid.innerHTML = '<p>API quota exceeded. Please try again later.</p>';
        } else {
            videoGrid.innerHTML = '<p>Failed to load videos. Please try again later.</p>';
        }
    }
};

// Helper function to parse ISO 8601 duration
const parseISO8601Duration = (duration) => {
    const match = duration.match(/PT(\d+H)?(\d+M)?(\d+S)?/);
    const hours = parseInt(match[1]) || 0;
    const minutes = parseInt(match[2]) || 0;
    const seconds = parseInt(match[3]) || 0;
    return hours * 3600 + minutes * 60 + seconds;
};

// Helper function to format seconds into H:M:S
const formatDuration = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${h > 0 ? h + 'h ' : ''}${m > 0 ? m + 'm ' : ''}${s}s`;
};

// Function to display videos
const displayVideos = (videos) => {
    videoGrid.innerHTML = ''; // Clear existing videos
    if (!videos || videos.length === 0) {
        videoGrid.innerHTML = '<p>No videos found. Please try a different query.</p>';
        return;
    }
    videos.forEach((video) => {
        const videoElement = document.createElement('div');
        videoElement.className = 'video';
        videoElement.innerHTML = `
            <iframe
                src="https://www.youtube.com/embed/${video.id}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
            ></iframe>
            <p>${video.title}</p>
            <p>Duration: ${formatDuration(video.duration)}</p>
        `;
        videoGrid.appendChild(videoElement);
    });
};

// Event Listener for Search Button
searchButton.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (query) {
        fetchVideos(query);
    }
});

// Event Listener for Keyword Buttons
keywordButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const query = button.getAttribute('data-keyword');
        fetchVideos(query);
    });
});

// Event Listener for Add Keyword Button
addKeywordButton.addEventListener('click', () => {
    const newKeyword = newKeywordInput.value.trim();
    if (newKeyword) {
        const newButton = document.createElement('button');
        newButton.className = 'keyword-btn';
        newButton.setAttribute('data-keyword', newKeyword);
        newButton.textContent = newKeyword;
        newButton.addEventListener('click', () => fetchVideos(newKeyword));
        keywordContainer.appendChild(newButton);
        newKeywordInput.value = ''; // Clear input
    }
});

// Event Listener for Sort Options
sortOptions.addEventListener('change', () => {
    const sortBy = sortOptions.value; // Get selected sort option
    fetchVideos('AI Tools for Developers', sortBy);
});

// Load default videos on page load
fetchVideos('AI Tools for Developers');
