// Check if we need to auto-analyze a movie (coming from movies page)
window.addEventListener('DOMContentLoaded', function() {
    const storedMovie = sessionStorage.getItem('analyzeMovie');
    if (storedMovie) {
        const movie = JSON.parse(storedMovie);
        movieSearch.value = movie.title;
        sessionStorage.removeItem('analyzeMovie');
        
        // Wait for movies to load, then analyze
        setTimeout(() => {
            analyzeMovie(movie.id);
        }, 1000);
    }
});
// API Base URL

// DOM Elements
const movieSearch = document.getElementById('movieSearch');
const searchBtn = document.getElementById('searchBtn');
const suggestions = document.getElementById('suggestions');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const errorDiv = document.getElementById('error');

// Movie data cache
let allMovies = [];

// Load all movies on page load
async function loadMovies() {
    try {
        const response = await fetch(`${API_URL}/api/movies`);
        const data = await response.json();
        
        if (data.success) {
            allMovies = data.movies;
            console.log(`✅ Loaded ${allMovies.length} movies`);
        }
    } catch (error) {
        console.error('Error loading movies:', error);
        showError('Failed to load movies. Please make sure the backend is running.');
    }
}

// Show suggestions as user types
movieSearch.addEventListener('input', function() {
    const query = this.value.trim().toLowerCase();
    
    if (query.length === 0) {
        suggestions.innerHTML = '';
        suggestions.classList.add('hidden');
        return;
    }
    
    // Filter movies based on search query
    const filtered = allMovies.filter(movie => 
        movie.title.toLowerCase().includes(query)
    ).slice(0, 10); // Show max 10 suggestions
    
    if (filtered.length > 0) {
        displaySuggestions(filtered);
    } else {
        suggestions.innerHTML = '<div style="padding: 15px; text-align: center; color: #999;">No movies found</div>';
        suggestions.classList.remove('hidden');
    }
});

// Display suggestions dropdown
function displaySuggestions(movies) {
    suggestions.innerHTML = movies.map(movie => `
        <div class="suggestion-item" data-movie-id="${movie.id}">
            <div class="suggestion-title">${movie.title}</div>
            <div class="suggestion-meta">${movie.year} • ${movie.genre} • ⭐ ${movie.rating}</div>
        </div>
    `).join('');
    
    suggestions.classList.remove('hidden');
    
    // Add click event to each suggestion
    document.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', function() {
            const movieId = this.getAttribute('data-movie-id');
            const movieTitle = this.querySelector('.suggestion-title').textContent;
            
            movieSearch.value = movieTitle;
            suggestions.innerHTML = '';
            suggestions.classList.add('hidden');
            
            analyzeMovie(movieId);
        });
    });
}

// Hide suggestions when clicking outside
document.addEventListener('click', function(e) {
    if (!movieSearch.contains(e.target) && !suggestions.contains(e.target)) {
        suggestions.innerHTML = '';
        suggestions.classList.add('hidden');
    }
});

// Search button click
searchBtn.addEventListener('click', function() {
    const query = movieSearch.value.trim();
    
    if (query.length === 0) {
        showError('Please enter a movie name');
        return;
    }
    
    // Find exact match
    const movie = allMovies.find(m => 
        m.title.toLowerCase() === query.toLowerCase()
    );
    
    if (movie) {
        analyzeMovie(movie.id);
    } else {
        showError(`Movie "${query}" not found. Please select from suggestions.`);
    }
});

// Enter key to search
movieSearch.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchBtn.click();
    }
});

// Analyze movie sentiment
async function analyzeMovie(movieId) {
    // Hide previous results and errors
    results.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loading.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_URL}/api/analyze/${movieId}`);
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Failed to analyze movie');
        }
    } catch (error) {
        console.error('Error analyzing movie:', error);
        showError('Failed to analyze movie. Please check if the backend is running.');
    } finally {
        loading.classList.add('hidden');
    }
}

// Display analysis results
function displayResults(data) {
    const { movie, analysis, sample_reviews } = data;
    
    // Movie Info
    document.getElementById('movieTitle').textContent = movie.title;
    document.getElementById('movieYear').textContent = `📅 ${movie.year}`;
    document.getElementById('movieGenre').textContent = `🎭 ${movie.genre}`;
    document.getElementById('movieRating').textContent = `⭐ ${movie.rating}/10`;
    
    // Verdict
    const verdictBadge = document.getElementById('verdictBadge');
    verdictBadge.textContent = analysis.verdict;
    
    // Color code the verdict
    if (analysis.verdict === 'Good Movie') {
        verdictBadge.style.color = '#28a745';
    } else if (analysis.verdict === 'Bad Movie') {
        verdictBadge.style.color = '#dc3545';
    } else {
        verdictBadge.style.color = '#ffc107';
    }
    
    document.getElementById('verdictReason').textContent = analysis.reason;
    
    // Statistics
    document.getElementById('positivePercent').textContent = `${analysis.positive_percent}%`;
    document.getElementById('positiveCount').textContent = `${analysis.positive_count} reviews`;
    
    document.getElementById('neutralPercent').textContent = `${analysis.neutral_percent}%`;
    document.getElementById('neutralCount').textContent = `${analysis.neutral_count} reviews`;
    
    document.getElementById('negativePercent').textContent = `${analysis.negative_percent}%`;
    document.getElementById('negativeCount').textContent = `${analysis.negative_count} reviews`;
    
    // Progress bars
    document.getElementById('positiveBar').style.width = `${analysis.positive_percent}%`;
    document.getElementById('neutralBar').style.width = `${analysis.neutral_percent}%`;
    document.getElementById('negativeBar').style.width = `${analysis.negative_percent}%`;
    
    // Total reviews
    document.getElementById('totalReviews').textContent = analysis.total_reviews;
    
    // Sample Reviews
    displaySampleReviews('positiveReviews', sample_reviews.positive);
    displaySampleReviews('negativeReviews', sample_reviews.negative);
    
    // Show results
    results.classList.remove('hidden');
    
    // Smooth scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display sample reviews
function displaySampleReviews(elementId, reviews) {
    const container = document.getElementById(elementId);
    
    if (reviews.length === 0) {
        container.innerHTML = '<p style="color: #999; font-style: italic;">No reviews available</p>';
        return;
    }
    
    container.innerHTML = reviews.map(review => `
        <div class="review-card">
            <div class="review-title">${review.review_title}</div>
            <div class="review-text">${review.review_text}</div>
            <div class="review-rating">Rating: ${review.rating}/10 • Confidence: ${(review.confidence * 100).toFixed(1)}%</div>
        </div>
    `).join('');
}

// Show error message
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
    results.classList.add('hidden');
    loading.classList.add('hidden');
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        errorDiv.classList.add('hidden');
    }, 5000);
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', function() {
    console.log('🎬 Movie Sentiment Analyzer loaded');
    loadMovies();
});