# import sqlite3
# import hashlib
# import os
# from datetime import datetime

# class Database:
#     def __init__(self):
#         # Get database path
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         project_dir = os.path.dirname(script_dir)
#         self.db_path = os.path.join(project_dir, 'users.db')
        
#         # Initialize database
#         self.init_database()
    
#     def get_connection(self):
#         """Create database connection"""
#         conn = sqlite3.connect(self.db_path, timeout=10, check_same_thread=False)
#         conn.row_factory = sqlite3.Row  # Return rows as dictionaries
#         return conn
    
#     def init_database(self):
#         """Create tables if they don't exist"""
#         conn = self.get_connection()
#         cursor = conn.cursor()
        
#         # Create users table
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE NOT NULL,
#                 email TEXT UNIQUE NOT NULL,
#                 password TEXT NOT NULL,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 last_login TIMESTAMP
#             )
#         ''')
        
#         # Create search history table
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS search_history (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_id INTEGER NOT NULL,
#                 movie_id TEXT NOT NULL,
#                 movie_title TEXT NOT NULL,
#                 searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 FOREIGN KEY (user_id) REFERENCES users (id)
#             )
#         ''')
        
#         conn.commit()
#         conn.close()
        
#         print("✅ Database initialized successfully!")
    
#     def hash_password(self, password):
#         """Hash password using SHA-256"""
#         return hashlib.sha256(password.encode()).hexdigest()
    
#     def create_user(self, username, email, password):
#         """Create a new user"""
#         conn = None
#         try:
#             conn = self.get_connection()
#             cursor = conn.cursor()
            
#             hashed_password = self.hash_password(password)
            
#             cursor.execute('''
#                 INSERT INTO users (username, email, password)
#                 VALUES (?, ?, ?)
#             ''', (username, email, hashed_password))
            
#             conn.commit()
#             user_id = cursor.lastrowid
            
#             return {
#                 'success': True,
#                 'message': 'User created successfully',
#                 'user_id': user_id
#             }
        
#         except sqlite3.IntegrityError as e:
#             if 'username' in str(e):
#                 return {'success': False, 'message': 'Username already exists'}
#             elif 'email' in str(e):
#                 return {'success': False, 'message': 'Email already exists'}
#             else:
#                 return {'success': False, 'message': 'Database error'}
        
#         except Exception as e:
#             return {'success': False, 'message': str(e)}
        
#         finally:
#             if conn:
#                 conn.close()
    
#     def verify_user(self, username, password):
#         """Verify user credentials"""
#         try:
#             conn = self.get_connection()
#             cursor = conn.cursor()
            
#             hashed_password = self.hash_password(password)
            
#             cursor.execute('''
#                 SELECT id, username, email, created_at
#                 FROM users
#                 WHERE username = ? AND password = ?
#             ''', (username, hashed_password))
            
#             user = cursor.fetchone()
            
#             if user:
#                 # Update last login
#                 cursor.execute('''
#                     UPDATE users
#                     SET last_login = ?
#                     WHERE id = ?
#                 ''', (datetime.now(), user['id']))
                
#                 conn.commit()
#                 conn.close()
                
#                 return {
#                     'success': True,
#                     'user': {
#                         'id': user['id'],
#                         'username': user['username'],
#                         'email': user['email'],
#                         'created_at': user['created_at']
#                     }
#                 }
#             else:
#                 conn.close()
#                 return {'success': False, 'message': 'Invalid username or password'}
        
#         except Exception as e:
#             return {'success': False, 'message': str(e)}
    
#     def get_user_by_id(self, user_id):
#         """Get user information by ID"""
#         try:
#             conn = self.get_connection()
#             cursor = conn.cursor()
            
#             cursor.execute('''
#                 SELECT id, username, email, created_at, last_login
#                 FROM users
#                 WHERE id = ?
#             ''', (user_id,))
            
#             user = cursor.fetchone()
#             conn.close()
            
#             if user:
#                 return {
#                     'success': True,
#                     'user': dict(user)
#                 }
#             else:
#                 return {'success': False, 'message': 'User not found'}
        
#         except Exception as e:
#             return {'success': False, 'message': str(e)}
    
#     def add_search_history(self, user_id, movie_id, movie_title):
#         """Add a search to user's history"""
#         try:
#             conn = self.get_connection()
#             cursor = conn.cursor()
            
#             cursor.execute('''
#                 INSERT INTO search_history (user_id, movie_id, movie_title)
#                 VALUES (?, ?, ?)
#             ''', (user_id, movie_id, movie_title))
            
#             conn.commit()
#             conn.close()
            
#             return {'success': True, 'message': 'Search saved to history'}
        
#         except Exception as e:
#             return {'success': False, 'message': str(e)}
    
#     def get_search_history(self, user_id, limit=10):
#         """Get user's search history"""
#         try:
#             conn = self.get_connection()
#             cursor = conn.cursor()
            
#             cursor.execute('''
#                 SELECT movie_id, movie_title, searched_at
#                 FROM search_history
#                 WHERE user_id = ?
#                 ORDER BY searched_at DESC
#                 LIMIT ?
#             ''', (user_id, limit))
            
#             history = cursor.fetchall()
#             conn.close()
            
#             return {
#                 'success': True,
#                 'history': [dict(row) for row in history]
#             }
        
#         except Exception as e:
#             return {'success': False, 'message': str(e)}
        
#     def init_database(self):
#         """Create tables if they don't exist"""
#         conn = self.get_connection()
#         cursor = conn.cursor()
        
#         # ... existing tables ...
        
#         # User reviews table
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS user_reviews (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user_id INTEGER NOT NULL,
#                 movie_id TEXT NOT NULL,
#                 movie_title TEXT NOT NULL,
#                 rating INTEGER NOT NULL,
#                 review_text TEXT NOT NULL,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 FOREIGN KEY (user_id) REFERENCES users (id)
#             )
#         ''')
        
#         conn.commit()
#         conn.close()

#     def add_user_review(self, user_id, movie_id, movie_title, rating, review_text):
#         """Add a user review"""
#         try:
#             conn = self.get_connection()
#             cursor = conn.cursor()
            
#             cursor.execute('''
#                 INSERT INTO user_reviews (user_id, movie_id, movie_title, rating, review_text)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (user_id, movie_id, movie_title, rating, review_text))
            
#             conn.commit()
#             conn.close()
            
#             return {'success': True, 'message': 'Review submitted successfully'}
#         except Exception as e:
#             return {'success': False, 'message': str(e)}

#     def get_user_reviews(self, movie_id):
#         """Get user reviews for a movie"""
#         try:
#             conn = self.get_connection()
#             cursor = conn.cursor()
            
#             cursor.execute('''
#                 SELECT ur.rating, ur.review_text, ur.created_at, u.username
#                 FROM user_reviews ur
#                 JOIN users u ON ur.user_id = u.id
#                 WHERE ur.movie_id = ?
#                 ORDER BY ur.created_at DESC
#             ''', (movie_id,))
            
#             reviews = cursor.fetchall()
#             conn.close()
            
#             return {
#                 'success': True,
#                 'reviews': [dict(row) for row in reviews]
#             }
#         except Exception as e:
#             return {'success': False, 'message': str(e)}

    

# # Test the database
# if __name__ == "__main__":
#     print("="*70)
#     print("TESTING DATABASE")
#     print("="*70)
    
#     db = Database()
    
#     # Test create user
#     print("\n--- Testing User Creation ---")
#     result = db.create_user("testuser", "test@example.com", "password123")
#     print(result)
    
#     # Test login
#     print("\n--- Testing User Login ---")
#     result = db.verify_user("testuser", "password123")
#     print(result)
    
#     # Test wrong password
#     print("\n--- Testing Wrong Password ---")
#     result = db.verify_user("testuser", "wrongpassword")
#     print(result)
    
#     print("\n" + "="*70)
#     print("✅ DATABASE TESTING COMPLETE!")
#     print("="*70)




import hashlib
import os
from datetime import datetime

# Check if running on Render (production)
USE_POSTGRES = os.environ.get('RENDER') is not None

if USE_POSTGRES:
    import psycopg2
    from psycopg2.extras import RealDictCursor
else:
    import sqlite3

class Database:
    def __init__(self):
        if USE_POSTGRES:
            # PostgreSQL connection (production)
            self.db_url = os.environ.get('DATABASE_URL')
            if self.db_url and self.db_url.startswith('postgres://'):
                self.db_url = self.db_url.replace('postgres://', 'postgresql://', 1)
        else:
            # SQLite connection (local)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(script_dir)
            self.db_path = os.path.join(project_dir, 'users.db')
        
        self.init_database()
    
    def get_connection(self):
        """Create database connection"""
        if USE_POSTGRES:
            conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
            return conn
        else:
            conn = sqlite3.connect(self.db_path, timeout=10, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            return conn
    
    def init_database(self):
        """Create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if USE_POSTGRES:
            # PostgreSQL syntax
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    movie_id VARCHAR(255) NOT NULL,
                    movie_title VARCHAR(255) NOT NULL,
                    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_reviews (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    movie_id VARCHAR(255) NOT NULL,
                    movie_title VARCHAR(255) NOT NULL,
                    rating INTEGER NOT NULL,
                    review_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
        else:
            # SQLite syntax (local)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    movie_id TEXT NOT NULL,
                    movie_title TEXT NOT NULL,
                    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    movie_id TEXT NOT NULL,
                    movie_title TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    review_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized successfully!")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password):
        """Create a new user"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            if USE_POSTGRES:
                cursor.execute('''
                    INSERT INTO users (username, email, password)
                    VALUES (%s, %s, %s) RETURNING id
                ''', (username, email, hashed_password))
                user_id = cursor.fetchone()['id']
            else:
                cursor.execute('''
                    INSERT INTO users (username, email, password)
                    VALUES (?, ?, ?)
                ''', (username, email, hashed_password))
                user_id = cursor.lastrowid
            
            conn.commit()
            
            return {
                'success': True,
                'message': 'User created successfully',
                'user_id': user_id
            }
        
        except Exception as e:
            error_msg = str(e).lower()
            if 'username' in error_msg or 'duplicate' in error_msg:
                return {'success': False, 'message': 'Username already exists'}
            elif 'email' in error_msg:
                return {'success': False, 'message': 'Email already exists'}
            else:
                return {'success': False, 'message': f'Database error: {str(e)}'}
        
        finally:
            if conn:
                conn.close()
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            if USE_POSTGRES:
                cursor.execute('''
                    SELECT id, username, email, created_at
                    FROM users
                    WHERE username = %s AND password = %s
                ''', (username, hashed_password))
            else:
                cursor.execute('''
                    SELECT id, username, email, created_at
                    FROM users
                    WHERE username = ? AND password = ?
                ''', (username, hashed_password))
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                if USE_POSTGRES:
                    cursor.execute('''
                        UPDATE users
                        SET last_login = %s
                        WHERE id = %s
                    ''', (datetime.now(), user['id']))
                else:
                    cursor.execute('''
                        UPDATE users
                        SET last_login = ?
                        WHERE id = ?
                    ''', (datetime.now(), user['id']))
                
                conn.commit()
                
                return {
                    'success': True,
                    'user': dict(user)
                }
            else:
                return {'success': False, 'message': 'Invalid username or password'}
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            if conn:
                conn.close()
    
    def get_user_by_id(self, user_id):
        """Get user information by ID"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                cursor.execute('''
                    SELECT id, username, email, created_at, last_login
                    FROM users
                    WHERE id = %s
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT id, username, email, created_at, last_login
                    FROM users
                    WHERE id = ?
                ''', (user_id,))
            
            user = cursor.fetchone()
            
            if user:
                return {'success': True, 'user': dict(user)}
            else:
                return {'success': False, 'message': 'User not found'}
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            if conn:
                conn.close()
    
    def add_search_history(self, user_id, movie_id, movie_title):
        """Add a search to user's history"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                cursor.execute('''
                    INSERT INTO search_history (user_id, movie_id, movie_title)
                    VALUES (%s, %s, %s)
                ''', (user_id, movie_id, movie_title))
            else:
                cursor.execute('''
                    INSERT INTO search_history (user_id, movie_id, movie_title)
                    VALUES (?, ?, ?)
                ''', (user_id, movie_id, movie_title))
            
            conn.commit()
            return {'success': True, 'message': 'Search saved to history'}
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            if conn:
                conn.close()
    
    def get_search_history(self, user_id, limit=10):
        """Get user's search history"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                cursor.execute('''
                    SELECT movie_id, movie_title, searched_at
                    FROM search_history
                    WHERE user_id = %s
                    ORDER BY searched_at DESC
                    LIMIT %s
                ''', (user_id, limit))
            else:
                cursor.execute('''
                    SELECT movie_id, movie_title, searched_at
                    FROM search_history
                    WHERE user_id = ?
                    ORDER BY searched_at DESC
                    LIMIT ?
                ''', (user_id, limit))
            
            history = cursor.fetchall()
            
            return {
                'success': True,
                'history': [dict(row) for row in history]
            }
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            if conn:
                conn.close()
    
    def add_user_review(self, user_id, movie_id, movie_title, rating, review_text):
        """Add a user review"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                cursor.execute('''
                    INSERT INTO user_reviews (user_id, movie_id, movie_title, rating, review_text)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (user_id, movie_id, movie_title, rating, review_text))
            else:
                cursor.execute('''
                    INSERT INTO user_reviews (user_id, movie_id, movie_title, rating, review_text)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, movie_id, movie_title, rating, review_text))
            
            conn.commit()
            return {'success': True, 'message': 'Review submitted successfully'}
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            if conn:
                conn.close()
    
    def get_user_reviews(self, movie_id):
        """Get user reviews for a movie"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                cursor.execute('''
                    SELECT ur.rating, ur.review_text, ur.created_at, u.username
                    FROM user_reviews ur
                    JOIN users u ON ur.user_id = u.id
                    WHERE ur.movie_id = %s
                    ORDER BY ur.created_at DESC
                ''', (movie_id,))
            else:
                cursor.execute('''
                    SELECT ur.rating, ur.review_text, ur.created_at, u.username
                    FROM user_reviews ur
                    JOIN users u ON ur.user_id = u.id
                    WHERE ur.movie_id = ?
                    ORDER BY ur.created_at DESC
                ''', (movie_id,))
            
            reviews = cursor.fetchall()
            
            return {
                'success': True,
                'reviews': [dict(row) for row in reviews]
            }
        
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
        finally:
            if conn:
                conn.close()