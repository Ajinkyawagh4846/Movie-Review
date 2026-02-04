import requests
import json
import os

TMDB_API_KEY = '5b000e59e2ee1c6ad07067f46b5490c5'  # Your real key
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Cache directory
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(movie_id):
    return os.path.join(CACHE_DIR, f"{movie_id}.json")

def tmdb_search_movie(title, movie_id=None):  # ✅ Changed name
    """Search with caching"""
    # Check cache first
    if movie_id:
        cache_file = get_cache_path(movie_id)
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
    
    # API call
    try:
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {'api_key': TMDB_API_KEY, 'query': title}
        response = requests.get(url, params=params, timeout=3)
        data = response.json()
        
        if data.get('results'):
            movie = data['results'][0]
            result = {
                'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get('poster_path') else None,
                'backdrop': f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path', '')}" if movie.get('backdrop_path') else None,
                'tmdb_id': movie['id']
            }
            
            # Save to cache
            if movie_id:
                with open(get_cache_path(movie_id), 'w') as f:
                    json.dump(result, f)
            
            return result
    except Exception as e:
        print(f"TMDb API error: {e}")
    
    return None

def get_trailer(tmdb_id):
    """Get YouTube trailer"""
    try:
        url = f"{TMDB_BASE_URL}/movie/{tmdb_id}/videos"
        params = {'api_key': TMDB_API_KEY}
        response = requests.get(url, params=params, timeout=3)
        data = response.json()
        
        for video in data.get('results', []):
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                return f"https://www.youtube.com/watch?v={video['key']}"
    except Exception as e:
        print(f"Trailer fetch error: {e}")
    
    return None