import hashlib
import os
from datetime import datetime
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://jrcixbtbintaylznzemt.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpyY2l4YnRiaW50YXlsem56ZW10Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDIxOTA5NiwiZXhwIjoyMDg1Nzk1MDk2fQ.fkzDvypLVjerG2igXZiFxBvvGu8WpkxyZ6viGqgCWVU')
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpyY2l4YnRiaW50YXlsem56ZW10Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAyMTkwOTYsImV4cCI6MjA4NTc5NTA5Nn0.KhSspVTxda141JbDlpY2QLQtt8FALr6rhqGnqi15n9Y
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseDB:
    def __init__(self):
        print("✅ Connected to Supabase")
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password):
        try:
            hashed_password = self.hash_password(password)
            
            result = supabase.table('users').insert({
                'username': username,
                'email': email,
                'password': hashed_password
            }).execute()
            
            return {
                'success': True,
                'message': 'User created successfully',
                'user_id': result.data[0]['id']
            }
        except Exception as e:
            error_msg = str(e).lower()
            if 'duplicate' in error_msg or 'unique' in error_msg:
                if 'username' in error_msg:
                    return {'success': False, 'message': 'Username already exists'}
                elif 'email' in error_msg:
                    return {'success': False, 'message': 'Email already exists'}
            return {'success': False, 'message': 'Registration failed'}
    
    def verify_user(self, username, password):
        try:
            hashed_password = self.hash_password(password)
            
            result = supabase.table('users').select('*').eq('username', username).eq('password', hashed_password).execute()
            
            if result.data and len(result.data) > 0:
                user = result.data[0]
                
                # Update last login
                supabase.table('users').update({'last_login': datetime.now().isoformat()}).eq('id', user['id']).execute()
                
                return {'success': True, 'user': user}
            else:
                return {'success': False, 'message': 'Invalid username or password'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_user_by_id(self, user_id):
        try:
            result = supabase.table('users').select('*').eq('id', user_id).execute()
            
            if result.data and len(result.data) > 0:
                return {'success': True, 'user': result.data[0]}
            else:
                return {'success': False, 'message': 'User not found'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def add_search_history(self, user_id, movie_id, movie_title):
        try:
            supabase.table('search_history').insert({
                'user_id': user_id,
                'movie_id': movie_id,
                'movie_title': movie_title
            }).execute()
            
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_search_history(self, user_id, limit=20):
        try:
            result = supabase.table('search_history').select('*').eq('user_id', user_id).order('searched_at', desc=True).limit(limit).execute()
            
            return {'success': True, 'history': result.data}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def add_user_review(self, user_id, movie_id, movie_title, rating, review_text):
        try:
            supabase.table('user_reviews').insert({
                'user_id': user_id,
                'movie_id': movie_id,
                'movie_title': movie_title,
                'rating': rating,
                'review_text': review_text
            }).execute()
            
            return {'success': True, 'message': 'Review submitted successfully'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_user_reviews(self, movie_id):
        try:
            result = supabase.table('user_reviews').select('*, users(username)').eq('movie_id', movie_id).order('created_at', desc=True).execute()
            
            reviews = []
            for item in result.data:
                reviews.append({
                    'rating': item['rating'],
                    'review_text': item['review_text'],
                    'created_at': item['created_at'],
                    'username': item['users']['username']
                })
            
            return {'success': True, 'reviews': reviews}
        except Exception as e:
            return {'success': False, 'message': str(e)}