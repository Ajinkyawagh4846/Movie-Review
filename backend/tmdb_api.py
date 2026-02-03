print("✅ CORRECT tmdb_api.py LOADED")

import requests

TMDB_API_KEY = '5b000e59e2ee1c6ad07067f46b5490c5'  # Replace with your key
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def tmdb_search_movie(title):    #changed function name from search_movie to tmdb_search_movie 
    """Search for movie on TMDb"""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': title
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['results']:
        movie = data['results'][0]
        return {
            'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get('poster_path') else None,
            'backdrop': f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path', '')}" if movie.get('backdrop_path') else None,
            'tmdb_id': movie['id']
        }
    return None

def get_trailer(tmdb_id):
    """Get YouTube trailer"""
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}/videos"
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    
    for video in data.get('results', []):
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None