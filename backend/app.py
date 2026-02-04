from flask import Flask, request, jsonify, session
from tmdb_api import tmdb_search_movie, get_trailer  # Updated import changed tmdb_search_movie
from flask_cors import CORS
import pandas as pd
import os
import sys
from datetime import datetime, timedelta
import secrets
from sentiment_model import SentimentAnalyzer
from supabase_db import SupabaseDB

# app = Flask(__name__)
# CORS(app, origins=["https://movie-reviewer-two.vercel.app"], supports_credentials=True)
# app.config['SECRET_KEY'] = secrets.token_hex(16)  # For session management
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session expires in 7 days

# CORS(app, supports_credentials=True, origins=['https://movie-reviewer-two.vercel.app','http://127.0.0.1:5500', 'http://localhost:5500', 'null'])  # Enable CORS with credentials
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Production session settings
# if os.environ.get('RENDER'):
#     app.config['SESSION_COOKIE_SECURE'] = True
#     app.config['SESSION_COOKIE_SAMESITE'] = 'None'
#     app.config['SESSION_COOKIE_HTTPONLY'] = True
# else:
#     app.config['SESSION_COOKIE_SECURE'] = False
#     app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# CORS configuration - MUST be after app initialization
if os.environ.get('RENDER'):
    # Production - allow Vercel domain
    # CORS - Allow your Vercel frontend
    CORS(app,
        supports_credentials=True,
        origins=[
            'https://movie-review-smnz.vercel.app/',  # Your Vercel URL
            'http://localhost:5500',
            'http://127.0.0.1:5500'
        ],
        allow_headers=['Content-Type', 'Authorization'],
        expose_headers=['Set-Cookie'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    # Session configuration
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
# CORS with proper credentials support
CORS(app, 
     supports_credentials=True,
     origins=['https://movie-review-smnz.vercel.app/', 'http://localhost:5500', 'http://127.0.0.1:5500'],
     allow_headers=['Content-Type'],
     expose_headers=['Set-Cookie'])
# Load datasets
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, 'data')


# Load combined dataset (original + Indian movies)
try:
    movies_df = pd.read_csv(os.path.join(data_dir, 'imdb_list_combined.csv'))
    print(f"✅ Loaded combined dataset: {len(movies_df)} movies")
except FileNotFoundError:
    movies_df = pd.read_csv(os.path.join(data_dir, 'imdb_list.csv'))
    print(f"✅ Loaded original dataset: {len(movies_df)} movies")
reviews_df = pd.read_csv(os.path.join(data_dir, 'imdb_reviews.csv'))

# Load trained model
analyzer = SentimentAnalyzer()
try:
    analyzer.load_model()
    print("✅ Sentiment model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)
movies_df = movies_df.fillna({
    'rating': 5.0,
    'genre': 'Not Available',
    'year': 2000,
    'poster_url': None,
    'has_reviews': False
})
movies_df['year'] = movies_df['year'].astype(int)
movies_df['rating'] = movies_df['rating'].astype(float)
# Initialize database
db = SupabaseDB()

# ========================================
# AUTHENTICATION ROUTES
# ========================================

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        # Username validation
        if len(username) < 3:
            return jsonify({
                'success': False,
                'message': 'Username must be at least 3 characters'
            }), 400
        
        # Password validation
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters'
            }), 400
        
        # Email validation (basic)
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Create user
        result = db.create_user(username, email, password)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Registration successful! Please login.'
            }), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Verify credentials
        result = db.verify_user(username, password)
        
        if result['success']:
            # Create session
            session.permanent = True
            session['user_id'] = result['user']['id']
            session['username'] = result['user']['username']
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': result['user']
            }), 200
        else:
            return jsonify(result), 401
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }), 200


@app.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user is logged in"""
    if 'user_id' in session:
        user_result = db.get_user_by_id(session['user_id'])
        if user_result['success']:
            return jsonify({
                'success': True,
                'logged_in': True,
                'user': user_result['user']
            }), 200
    
    return jsonify({
        'success': True,
        'logged_in': False
    }), 200


@app.route('/api/user/profile', methods=['GET'])
def get_profile():
    """Get user profile (requires login)"""
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Please login first'
        }), 401
    
    user_result = db.get_user_by_id(session['user_id'])
    
    if user_result['success']:
        return jsonify(user_result), 200
    else:
        return jsonify(user_result), 404


@app.route('/api/user/search-history', methods=['GET'])
def get_user_history():
    """Get user's search history (requires login)"""
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Please login first'
        }), 401
    
    limit = request.args.get('limit', 10, type=int)
    history_result = db.get_search_history(session['user_id'], limit)
    
    return jsonify(history_result), 200


# ========================================
# MOVIE ROUTES (Updated)
# ========================================

@app.route('/')
def home():
    return jsonify({
        'message': 'Movie Sentiment Analysis API',
        'total_movies': len(movies_df),
        'total_reviews': len(reviews_df),
        'status': 'running',
        'logged_in': 'user_id' in session
    })


@app.route('/api/movies', methods=['GET'])
def get_movies():
    """Return list of all movies"""
    movies_list = movies_df[['id', 'title', 'rating', 'genre', 'year']].to_dict('records')
    
    # Log for debugging
    print(f"Returning {len(movies_list)} movies")
    
    return jsonify({
        'success': True,
        'count': len(movies_list),
        'movies': movies_list
    })


@app.route('/api/search', methods=['GET'])
def search_movie():
    """Search for a movie by name"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'success': False, 'error': 'No search query provided'}), 400
    
    results = movies_df[movies_df['title'].str.contains(query, case=False, na=False)]
    
    if results.empty:
        return jsonify({'success': False, 'error': 'No movies found'}), 404
    
    movies_list = results[['id', 'title', 'rating', 'genre', 'year']].to_dict('records')
    
    return jsonify({
        'success': True,
        'count': len(movies_list),
        'movies': movies_list
    })


@app.route('/api/analyze/<movie_id>', methods=['GET'])
def analyze_movie(movie_id):
    """Analyze sentiment for a specific movie"""
    
    # Get movie details
    movie = movies_df[movies_df['id'] == movie_id]
    
    if movie.empty:
        return jsonify({'success': False, 'error': 'Movie not found'}), 404
    
    movie_info = movie.iloc[0].to_dict()
    
    # Save to search history if user is logged in
    # Save to search history if user is logged in
    if 'user_id' in session:
        db.add_search_history(session['user_id'], movie_id, movie_info['title'])
        print(f"✅ Saved search for user {session['user_id']}")
    # if 'user_id' in session:
    #     db.add_search_history(
    #         session['user_id'],
    #         movie_id,
    #         movie_info['title']
    #     )
    # Get all reviews for this movie
    # Get all reviews for this movie
    movie_reviews = reviews_df[reviews_df['imdb_id'] == movie_id]

    # Check if this movie has reviews
    if movie_reviews.empty:
        # Indian movie without reviews - show basic info only
        return jsonify({
            'success': True,
            'no_reviews': True,
            'movie': {
                'id': movie_info['id'],
                'title': movie_info['title'],
                'rating': float(movie_info['rating']),
                'genre': movie_info['genre'],
                'year': int(movie_info['year']),
                'poster_url': movie_info.get('poster_url', None)
            },
            'message': 'This movie is from our extended database. Sentiment analysis is not available, but you can see IMDb rating and details.'
        })
    
    # Save to search history if user is logged in
    # if 'user_id' in session:
    #     db.add_search_history(
    #         session['user_id'],
    #         movie_id,
    #         movie_info['title']
    #     )
    
    # Analyze sentiment for each review
    sentiments = []
    for _, review_row in movie_reviews.iterrows():
        sentiment_result = analyzer.predict_sentiment(review_row['review'])
        sentiments.append({
            'sentiment': sentiment_result['sentiment'],
            'sentiment_label': sentiment_result['sentiment_label'],
            'confidence': sentiment_result['confidence'],
            'rating': review_row['review_rating'],
            'review_title': review_row['review title'],
            'review_text': review_row['review'][:200] + '...'
        })
    
    # Calculate statistics
    total_reviews = len(sentiments)
    negative_count = sum(1 for s in sentiments if s['sentiment'] == 0)
    neutral_count = sum(1 for s in sentiments if s['sentiment'] == 1)
    positive_count = sum(1 for s in sentiments if s['sentiment'] == 2)
    
    negative_percent = (negative_count / total_reviews) * 100
    neutral_percent = (neutral_count / total_reviews) * 100
    positive_percent = (positive_count / total_reviews) * 100
    
    # Determine overall verdict
    if positive_percent > 50:
        verdict = "Good Movie"
        reason = f"This movie has {positive_percent:.1f}% positive reviews. Audiences generally enjoyed the film, praising its quality and entertainment value."
    elif negative_percent > 40:
        verdict = "Bad Movie"
        reason = f"This movie has {negative_percent:.1f}% negative reviews. Many viewers were disappointed with various aspects of the film."
    else:
        verdict = "Mixed Reviews"
        reason = f"This movie received mixed reactions with {positive_percent:.1f}% positive and {negative_percent:.1f}% negative reviews. Opinions are divided."
    
    # Get sample positive and negative reviews
    positive_samples = [s for s in sentiments if s['sentiment'] == 2][:2]
    negative_samples = [s for s in sentiments if s['sentiment'] == 0][:2]
    
    return jsonify({
        'success': True,
        'movie': {
            'id': movie_info['id'],
            'title': movie_info['title'],
            'rating': float(movie_info['rating']),
            'genre': movie_info['genre'],
            'year': int(movie_info['year'])
        },
        'analysis': {
            'total_reviews': total_reviews,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_count': positive_count,
            'negative_percent': round(negative_percent, 2),
            'neutral_percent': round(neutral_percent, 2),
            'positive_percent': round(positive_percent, 2),
            'verdict': verdict,
            'reason': reason
        },
        'sample_reviews': {
            'positive': positive_samples,
            'negative': negative_samples
        }
    })


@app.route('/api/movie-media/<movie_id>', methods=['GET'])
def get_movie_media(movie_id):
    """Get poster and trailer for a movie"""
    movie = movies_df[movies_df['id'] == movie_id]
    if movie.empty:
        return jsonify({'success': False}), 404
    
    title = movie.iloc[0]['title']
    tmdb_data = tmdb_search_movie(title)  #changed function name from search_movie to tmdb_search_movie
    
    if tmdb_data:
        trailer = get_trailer(tmdb_data['tmdb_id'])
        return jsonify({
            'success': True,
            'poster': tmdb_data['poster'],
            'backdrop': tmdb_data['backdrop'],
            'trailer': trailer
        })
    
    return jsonify({'success': False}), 404

# @app.route('/api/submit-review', methods=['POST'])
# def submit_review():
#     """Submit user review"""
#     if 'user_id' not in session:
#         return jsonify({'success': False, 'message': 'Please login first'}), 401
    
#     data = request.get_json()
#     movie_id = data.get('movie_id')
#     movie_title = data.get('movie_title')
#     rating = data.get('rating')
#     review_text = data.get('review_text', '').strip()
    
#     if not all([movie_id, movie_title, rating, review_text]):
#         return jsonify({'success': False, 'message': 'All fields required'}), 400
    
#     if not (1 <= int(rating) <= 10):
#         return jsonify({'success': False, 'message': 'Rating must be 1-10'}), 400
    
#     result = db.add_user_review(session['user_id'], movie_id, movie_title, int(rating), review_text)
#     return jsonify(result)

# @app.route('/api/user-reviews/<movie_id>', methods=['GET'])
# def get_user_movie_reviews(movie_id):
#     """Get user reviews for a movie"""
#     result = db.get_user_reviews(movie_id)
#     return jsonify(result)

@app.route('/api/submit-review', methods=['POST'])
def submit_review():
    """Submit user review"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'}), 401
    
    try:
        data = request.get_json()
        movie_id = data.get('movie_id')
        movie_title = data.get('movie_title')
        rating = data.get('rating')
        review_text = data.get('review_text', '').strip()
        
        if not all([movie_id, movie_title, rating, review_text]):
            return jsonify({'success': False, 'message': 'All fields required'}), 400
        
        if not (1 <= int(rating) <= 10):
            return jsonify({'success': False, 'message': 'Rating must be 1-10'}), 400
        
        result = db.add_user_review(session['user_id'], movie_id, movie_title, int(rating), review_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/user-reviews/<movie_id>', methods=['GET'])
def get_user_movie_reviews(movie_id):
    """Get user reviews for a movie"""
    try:
        result = db.get_user_reviews(movie_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 STARTING MOVIE SENTIMENT ANALYSIS API")
    print("="*70)
    print(f"Total Movies: {len(movies_df)}")
    print(f"Total Reviews: {len(reviews_df)}")
    print("\n✅ Server starting on http://127.0.0.1:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5000)
    # app = Flask(__name__)
