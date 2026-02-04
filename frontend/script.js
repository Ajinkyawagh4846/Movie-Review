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
    // Check if movie has no reviews
if (data.no_reviews) {
    // Show basic info without sentiment
    document.getElementById('movieTitle').textContent = data.movie.title;
    document.getElementById('movieYear').textContent = `📅 ${data.movie.year}`;
    document.getElementById('movieGenre').textContent = `🎭 ${data.movie.genre}`;
    document.getElementById('movieRating').textContent = `⭐ ${data.movie.rating}/10 (IMDb)`;
    
    // Show message instead of sentiment
    results.innerHTML = `
        <div class="movie-info">
            <h2>${data.movie.title}</h2>
            <div class="movie-details">
                <span>📅 ${data.movie.year}</span>
                <span>🎭 ${data.movie.genre}</span>
                <span>⭐ ${data.movie.rating}/10 (IMDb)</span>
            </div>
        </div>
        <div style="text-align: center; padding: 40px; background: #fff3cd; border-radius: 15px; margin: 20px 0;">
            <h3 style="color: #856404;">ℹ️ ${data.message}</h3>
            <p style="margin-top: 15px;">IMDb Rating: <strong>${data.movie.rating}/10</strong></p>
        </div>
    `;
    
    results.classList.remove('hidden');
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    return;
}
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
        verdictBadge.style.color = '#ff0000ff';
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

    fetchMovieMedia(data.movie.id);
    // Call this in displayResults function
    // loadUserReviews(data.movie.id);
    // Load user reviews
    loadUserReviews(data.movie.id, data.movie.title);
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


// Fetch movie poster and trailer
async function fetchMovieMedia(movieId) {
    try {
        const response = await fetch(`${API_URL}/api/movie-media/${movieId}`);
        const data = await response.json();
        
        if (data.success && data.poster) {
            // Add poster to movie info
            const movieInfo = document.querySelector('.movie-info');
            const posterHTML = `
                <div style="text-align: center; margin: 20px 0;">
                    <img src="${data.poster}" alt="Movie Poster" style="max-width: 300px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                </div>
            `;
            movieInfo.insertAdjacentHTML('afterbegin', posterHTML);
            
            // Add trailer button if available
            if (data.trailer) {
                const trailerBtn = `
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="${data.trailer}" target="_blank" class="btn-primary" style="text-decoration: none; display: inline-block;">
                            ▶️ Watch Trailer
                        </a>
                    </div>
                `;
                movieInfo.insertAdjacentHTML('beforeend', trailerBtn);
            }
        }
    } catch (error) {
        console.log('Could not load movie media');
    }
}
// --------------------------------------------------------------------------------------------------------
// let currentMovieId = null;

// // After displaying results, load user reviews
// async function loadUserReviews(movieId) {
//     currentMovieId = movieId;
    
//     const response = await fetch(`${API_URL}/api/user-reviews/${movieId}`);
//     const data = await response.json();
    
//     document.getElementById('userReviewsSection').classList.remove('hidden');
    
//     // Check if logged in
//     const sessionCheck = await fetch(`${API_URL}/api/check-session`, {credentials: 'include'});
//     const session = await sessionCheck.json();
    
//     if (session.logged_in) {
//         document.getElementById('submitReviewForm').classList.remove('hidden');
//     }
    
//     if (data.success && data.reviews.length > 0) {
//         displayUserReviews(data.reviews);
//     }
// }

// function displayUserReviews(reviews) {
//     const html = reviews.map(r => `
//         <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid var(--primary-color);">
//             <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
//                 <strong>👤 ${r.username}</strong>
//                 <span>⭐ ${r.rating}/10</span>
//             </div>
//             <p style="color: #666; line-height: 1.6;">${r.review_text}</p>
//             <small style="color: #999;">${new Date(r.created_at).toLocaleDateString()}</small>
//         </div>
//     `).join('');
    
//     document.getElementById('userReviewsList').innerHTML = html;
// }

// async function submitUserReview() {
//     const rating = document.getElementById('userRating').value;
//     const reviewText = document.getElementById('userReviewText').value;
    
//     if (!rating || !reviewText) {
//         alert('Please provide both rating and review');
//         return;
//     }
    
//     const response = await fetch(`${API_URL}/api/submit-review`, {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         credentials: 'include',
//         body: JSON.stringify({
//             movie_id: currentMovieId,
//             movie_title: document.getElementById('movieTitle').textContent,
//             rating: parseInt(rating),
//             review_text: reviewText
//         })
//     });
    
//     const data = await response.json();
//     alert(data.message);
    
//     if (data.success) {
//         document.getElementById('userRating').value = '';
//         document.getElementById('userReviewText').value = '';
//         loadUserReviews(currentMovieId);
//     }
// }


let currentMovieId = null;

// Load user reviews for a movie
async function loadUserReviews(movieId, movieTitle) {
    currentMovieId = movieId;
    currentMovieTitle = movieTitle;
    
    try {
        const response = await fetch(`${API_URL}/api/user-reviews/${movieId}`, {
            credentials: 'include'
        });
        const data = await response.json();
        
        document.getElementById('userReviewsSection').classList.remove('hidden');
        
        // Check if logged in to show submit form
        const sessionCheck = await fetch(`${API_URL}/api/check-session`, {
            credentials: 'include'
        });
        const session = await sessionCheck.json();
        
        if (session.logged_in) {
            document.getElementById('submitReviewForm').classList.remove('hidden');
        } else {
            document.getElementById('submitReviewForm').classList.add('hidden');
        }
        
        // Display reviews
        if (data.success && data.reviews && data.reviews.length > 0) {
            displayUserReviews(data.reviews);
            document.getElementById('noUserReviews').classList.add('hidden');
        } else {
            document.getElementById('userReviewsList').innerHTML = '';
            document.getElementById('noUserReviews').classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error loading user reviews:', error);
    }
}

// Display user reviews
function displayUserReviews(reviews) {
    const html = reviews.map(r => `
        <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid var(--primary-color); box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; align-items: center;">
                <strong style="color: var(--primary-color);">👤 ${r.username}</strong>
                <span style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; padding: 5px 12px; border-radius: 15px; font-weight: bold;">⭐ ${r.rating}/10</span>
            </div>
            <p style="color: #333; line-height: 1.6; margin: 10px 0;">${r.review_text}</p>
            <small style="color: #999;">${new Date(r.created_at).toLocaleDateString('en-US', {year: 'numeric', month: 'long', day: 'numeric'})}</small>
        </div>
    `).join('');
    
    document.getElementById('userReviewsList').innerHTML = html;
}

// Submit user review
async function submitUserReview() {
    const rating = document.getElementById('userRating').value;
    const reviewText = document.getElementById('userReviewText').value.trim();
    
    if (!rating || !reviewText) {
        alert('Please provide both rating and review');
        return;
    }
    
    if (reviewText.length < 10) {
        alert('Please write a review of at least 10 characters');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/submit-review`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({
                movie_id: currentMovieId,
                movie_title: currentMovieTitle,
                rating: parseInt(rating),
                review_text: reviewText
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✅ Review submitted successfully!');
            document.getElementById('userRating').value = '7';
            document.getElementById('userReviewText').value = '';
            loadUserReviews(currentMovieId, currentMovieTitle);
        } else {
            alert('❌ ' + data.message);
        }
    } catch (error) {
        alert('Failed to submit review. Please try again.');
        console.error(error);
    }
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', function() {
    console.log('🎬 Movie Sentiment Analyzer loaded');
    loadMovies();
});