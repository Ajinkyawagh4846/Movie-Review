
let allMovies = [];
let filteredMovies = [];

// Load movies on page load
document.addEventListener('DOMContentLoaded', function() {
    loadAllMovies();
    setupFilters();
});

// Load all movies from API
// async function loadAllMovies() {
//     try {
//         const response = await fetch(`${API_URL}/api/movies`);
//         const data = await response.json();
        
//         if (data.success) {
//             allMovies = data.movies;
//             filteredMovies = [...allMovies];
            
//             populateFilters();
//             displayMovies(filteredMovies);
            
//             document.getElementById('loadingMovies').classList.add('hidden');
//             document.getElementById('moviesGrid').classList.remove('hidden');
//         }
//     } catch (error) {
//         console.error('Error loading movies:', error);
//         document.getElementById('loadingMovies').innerHTML = '<p style="color: red;">Failed to load movies. Please refresh the page.</p>';
//     }
// }
async function loadAllMovies() {
    try {
        const response = await fetch(`${API_URL}/api/movies`, {
            credentials: 'include'
        });
        const data = await response.json();
        
        console.log('Movies API response:', data); // Debug log
        
        if (data.success) {
            allMovies = data.movies;
            filteredMovies = [...allMovies];
            
            populateFilters();
            displayMovies(filteredMovies);
            
            document.getElementById('loadingMovies').classList.add('hidden');
            document.getElementById('moviesGrid').classList.remove('hidden');
        } else {
            throw new Error('Failed to load movies');
        }
    } catch (error) {
        console.error('Error loading movies:', error);
        document.getElementById('loadingMovies').innerHTML = `
            <p style="color: red;">Failed to load movies. Please check:</p>
            <ul style="text-align: left; max-width: 400px; margin: 20px auto;">
                <li>Backend server is running (http://127.0.0.1:5000)</li>
                <li>Check browser console (F12) for errors</li>
            </ul>
            <button onclick="location.reload()" style="padding: 10px 20px; margin-top: 20px;">Retry</button>
        `;
    }
}
// Populate filter dropdowns
function populateFilters() {
    // Get unique genres
    const genresSet = new Set();
    allMovies.forEach(movie => {
        const genres = movie.genre.split(',').map(g => g.trim());
        genres.forEach(genre => genresSet.add(genre));
    });
    
    const genreFilter = document.getElementById('genreFilter');
    Array.from(genresSet).sort().forEach(genre => {
        const option = document.createElement('option');
        option.value = genre;
        option.textContent = genre;
        genreFilter.appendChild(option);
    });
    
    // Get unique years
    const yearsSet = new Set(allMovies.map(m => m.year));
    const yearFilter = document.getElementById('yearFilter');
    Array.from(yearsSet).sort((a, b) => b - a).forEach(year => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearFilter.appendChild(option);
    });
}

// Setup filter event listeners
function setupFilters() {
    document.getElementById('searchFilter').addEventListener('input', applyFilters);
    document.getElementById('genreFilter').addEventListener('change', applyFilters);
    document.getElementById('yearFilter').addEventListener('change', applyFilters);
    document.getElementById('sortFilter').addEventListener('change', applyFilters);
}

// Apply all filters
function applyFilters() {
    const searchTerm = document.getElementById('searchFilter').value.toLowerCase();
    const selectedGenre = document.getElementById('genreFilter').value;
    const selectedYear = document.getElementById('yearFilter').value;
    const sortBy = document.getElementById('sortFilter').value;
    
    // Filter movies
    filteredMovies = allMovies.filter(movie => {
        const matchesSearch = movie.title.toLowerCase().includes(searchTerm);
        const matchesGenre = !selectedGenre || movie.genre.includes(selectedGenre);
        const matchesYear = !selectedYear || movie.year == selectedYear;
        
        return matchesSearch && matchesGenre && matchesYear;
    });
    
    // Sort movies
    filteredMovies.sort((a, b) => {
        if (sortBy === 'title') {
            return a.title.localeCompare(b.title);
        } else if (sortBy === 'rating') {
            return b.rating - a.rating;
        } else if (sortBy === 'year') {
            return b.year - a.year;
        }
    });
    
    displayMovies(filteredMovies);
}

// Display movies
function displayMovies(movies) {
    const grid = document.getElementById('moviesGrid');
    const noResults = document.getElementById('noResults');
    
    if (movies.length === 0) {
        grid.classList.add('hidden');
        noResults.classList.remove('hidden');
        return;
    }
    
    grid.classList.remove('hidden');
    noResults.classList.add('hidden');
    
    grid.innerHTML = movies.map(movie => `
        <div class="movie-card" onclick="analyzeMovie('${movie.id}')">
            <div class="movie-title">${movie.title}</div>
            <div class="movie-meta">
                <div class="movie-meta-item">
                    📅 <strong>${movie.year}</strong>
                </div>
                <div class="movie-meta-item">
                    🎭 ${movie.genre}
                </div>
                <div class="movie-meta-item">
                    <span class="movie-rating">⭐ ${movie.rating}/10</span>
                </div>
            </div>
            <button class="analyze-btn" onclick="analyzeMovie('${movie.id}'); event.stopPropagation();">
                Analyze Sentiment
            </button>
        </div>
    `).join('');
}

// Analyze movie - redirect to search page
function analyzeMovie(movieId) {
    const movie = allMovies.find(m => m.id === movieId);
    if (movie) {
        // Store movie info in session storage
        sessionStorage.setItem('analyzeMovie', JSON.stringify(movie));
        window.location.href = 'search.html';
    }
}