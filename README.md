# 🎬 FilmReviewer - AI-Powered Movie Sentiment Analysis

<div align="center">

![FilmReviewer](https://img.shields.io/badge/FilmReviewer-AI%20Powered-blueviolet)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green)
![Machine Learning](https://img.shields.io/badge/ML-Sentiment%20Analysis-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Discover what people really think about your favorite movies through advanced AI sentiment analysis**

[Live Demo](https://movie-review-smnz.vercel.app/) • [Live Backend](https://movie-review-fqp4.onrender.com) • [Report Bug](https://github.com/Ajinkyawagh4846/movie-reviewer) • [Request Feature](https://github.com/Ajinkyawagh4846/movie-reviewer)

</div>

---

## 🎯 About The Project

**FilmReviewer** is an intelligent movie sentiment analysis platform that helps users make informed viewing decisions by analyzing thousands of movie reviews using advanced Natural Language Processing (NLP) and Machine Learning techniques.

### Why FilmReviewer?

- 🤖 **AI-Powered Analysis**: Uses ML models trained on 6,241+ real movie reviews
- 📊 **Comprehensive Insights**: Get detailed sentiment breakdowns (Positive, Neutral, Negative)
- 🎭 **Large Database**: Browse 249+ movies with full sentiment analysis, and 1000+ movies with ratings
- 🔐 **User Features**: Account system with search history and personalized recommendations
- 🌙 **Modern UI**: Beautiful, responsive interface with dark mode support
- 🚀 **Fast & Reliable**: Cached API responses for instant results
- ☁️ **Cloud Database**: Powered by Supabase for scalable data management

---

## ✨ Features

### Core Features
- ✅ **AI Sentiment Analysis** - 75% accuracy sentiment classification
- ✅ **Smart Search** - Autocomplete search with real-time suggestions
- ✅ **Browse Movies** - Filter by genre, year, rating with advanced sorting
- ✅ **Detailed Reports** - Percentage breakdowns with sample reviews
- ✅ **Movie Posters & Trailers** - Integration with TMDb API
- ✅ **User Authentication** - Secure login/registration system
- ✅ **Search History** - Track and revisit analyzed movies
- ✅ **User Reviews** - Submit and read community reviews
- ✅ **Dark Mode** - Toggle between light and dark themes
- ✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile

### Advanced Features
- 🎯 **Movie Recommendations** - Get similar movie suggestions
- 📈 **Visual Analytics** - Progress bars and statistical visualizations
- 💾 **Cloud Data Persistence** - Supabase PostgreSQL database
- ⚡ **API Caching** - Fast response times with intelligent caching
- 🔒 **Secure Authentication** - Password hashing with SHA-256
- 🌐 **Real-time Updates** - Community reviews sync instantly

---

## 🛠️ Tech Stack

### 🔹 Backend
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![REST API](https://img.shields.io/badge/REST-API-green)
![Session Auth](https://img.shields.io/badge/Authentication-Session--Based-orange)

### 🔹 Frontend
![HTML5](https://img.shields.io/badge/HTML5-Markup-orange?logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-Styling-blue?logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)
![Responsive Design](https://img.shields.io/badge/Responsive-Mobile--First-green)

### 🔹 Machine Learning & NLP
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikitlearn)
![NLTK](https://img.shields.io/badge/NLTK-NLP-green)
![TF-IDF](https://img.shields.io/badge/TF--IDF-Vectorization-blueviolet)
![Naive Bayes](https://img.shields.io/badge/Naive%20Bayes-Classifier-red)
![Text Preprocessing](https://img.shields.io/badge/Text-Preprocessing-lightgrey)

### 🔹 Database & Cloud
![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?logo=supabase)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![SQLite](https://img.shields.io/badge/SQLite-Local%20Dev-003B57?logo=sqlite)

### 🔹 APIs & External Services
![TMDb API](https://img.shields.io/badge/TMDb-Movie%20API-01B4E4)
![Supabase API](https://img.shields.io/badge/Supabase-REST%20API-3ECF8E)
![Fetch API](https://img.shields.io/badge/Fetch-API-green)

### 🔹 Deployment & Tools
![Render](https://img.shields.io/badge/Render-Backend%20Hosting-purple)
![Vercel](https://img.shields.io/badge/Vercel-Frontend%20Hosting-black?logo=vercel)
![Environment Variables](https://img.shields.io/badge/ENV-Variables-yellow)
![VS Code](https://img.shields.io/badge/VS%20Code-Editor-blue?logo=visualstudiocode)
![Git](https://img.shields.io/badge/Git-Version%20Control-orange?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git
- Supabase account (free tier)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Ajinkyawagh4846/movie-reviewer.git
cd movie-reviewer
```

2. **Set up Supabase Database**
   - Create account at [supabase.com](https://supabase.com)
   - Create new project
   - Go to SQL Editor and run:
```sql
   -- Create users table
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(255) UNIQUE NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       password VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT NOW(),
       last_login TIMESTAMP
   );
   
   -- Create search history table
   CREATE TABLE search_history (
       id SERIAL PRIMARY KEY,
       user_id INTEGER NOT NULL,
       movie_id VARCHAR(255) NOT NULL,
       movie_title VARCHAR(255) NOT NULL,
       searched_at TIMESTAMP DEFAULT NOW(),
       FOREIGN KEY (user_id) REFERENCES users (id)
   );
   
   -- Create user reviews table
   CREATE TABLE user_reviews (
       id SERIAL PRIMARY KEY,
       user_id INTEGER NOT NULL,
       movie_id VARCHAR(255) NOT NULL,
       movie_title VARCHAR(255) NOT NULL,
       rating INTEGER NOT NULL,
       review_text TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT NOW(),
       FOREIGN KEY (user_id) REFERENCES users (id)
   );
```
   - Copy your Project URL and service_role key from Settings → API

3. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
```

4. **Configure environment variables**
   
   Create `.env` file in backend folder:
```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_service_role_key
```

5. **Download NLTK data** (first time only)
```python
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

6. **Train the ML model** (if not already trained)
```bash
python sentiment_model.py
```

7. **Start the backend server**
```bash
python app.py
```

8. **Open the frontend**
   - Navigate to `frontend/index.html` in your browser
   - Or use Live Server extension in VS Code

9. **Access the application**
   - Frontend: `http://127.0.0.1:5500`
   - Backend API: `http://127.0.0.1:5000`

---

## 📖 Usage

### For Users

1. **Browse Movies** - Explore 1000+ movies with filters
2. **Search** - Type movie name and get instant suggestions
3. **Analyze** - Click on any movie to see sentiment analysis
4. **Create Account** - Sign up to save search history
5. **Submit Reviews** - Share your opinions with the community
6. **View History** - Access your past searches anytime

### For Developers
```python
# Example: Using the sentiment analysis API
import requests

response = requests.get('https://movie-review-fqp4.onrender.com/api/analyze/tt1431045')
data = response.json()

print(f"Movie: {data['movie']['title']}")
print(f"Verdict: {data['analysis']['verdict']}")
print(f"Positive: {data['analysis']['positive_percent']}%")
```

---

## 📁 Project Structure
```
filmreviewer/
│
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── sentiment_model.py      # ML model training & prediction
│   ├── supabase_db.py         # Supabase database operations
│   ├── tmdb_api.py            # TMDb API integration
│   ├── requirements.txt        # Python dependencies
│   └── cache/                  # API response cache
│
├── frontend/
│   ├── index.html             # Home page
│   ├── movies.html            # Browse movies page
│   ├── search.html            # Search & analyze page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── recent-searches.html   # Search history page
│   ├── style.css              # Main stylesheet
│   ├── config.js              # Configuration
│   ├── auth.js                # Authentication logic
│   ├── script.js              # Search functionality
│   └── movies.js              # Movies page logic
│
├── data/
│   ├── imdb_list.csv          # Movie metadata
│   └── imdb_reviews.csv       # Movie reviews dataset
│
├── models/
│   └── sentiment_model.pkl    # Trained ML model
│
└── README.md                  # Project documentation
```

---

## 🤖 Machine Learning Model

### Model Details
- **Algorithm**: Multinomial Naive Bayes
- **Feature Extraction**: TF-IDF (5000 features)
- **Training Data**: 6,241 movie reviews
- **Classes**: 3 (Negative, Neutral, Positive)
- **Accuracy**: 75%

### Data Preprocessing Pipeline
1. Text cleaning (lowercase, special character removal)
2. Tokenization
3. Stopword removal
4. TF-IDF vectorization

### Sentiment Classification
- **Negative (0)**: Ratings 1-4
- **Neutral (1)**: Ratings 5-7
- **Positive (2)**: Ratings 8-10

---

## 📡 API Documentation

### Base URL
```
Production: https://movie-review-fqp4.onrender.com
Development: http://127.0.0.1:5000
```

### Endpoints

#### Get All Movies
```http
GET /api/movies
```
Returns list of all movies with metadata

#### Search Movies
```http
GET /api/search?q=Deadpool
```
Search movies by title with autocomplete

#### Analyze Movie Sentiment
```http
GET /api/analyze/{movie_id}
```
Get detailed sentiment analysis for a specific movie

#### User Registration
```http
POST /api/register
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

#### User Login
```http
POST /api/login
Content-Type: application/json

{
  "username": "john",
  "password": "password123"
}
```

#### Submit Review
```http
POST /api/submit-review
Content-Type: application/json

{
  "movie_id": "tt1431045",
  "movie_title": "Deadpool",
  "rating": 9,
  "review_text": "Amazing movie!"
}
```

#### Get User Reviews
```http
GET /api/user-reviews/{movie_id}
```

---

## 🌐 Deployment

### Architecture Overview
```
┌─────────────────┐
│   Vercel        │
│   (Frontend)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐      ┌──────────────┐
│   Render        │ ───→ │  Supabase    │
│   (Backend/ML)  │      │  (Database)  │
└─────────────────┘      └──────────────┘
```

### Backend Deployment (Render)

1. **Prerequisites**
   - GitHub account
   - Render account
   - Supabase project setup

2. **Steps**
   - Push code to GitHub
   - Create new Web Service on Render
   - Connect GitHub repository
   - Set root directory to `backend`
   - Add environment variables:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `RENDER=true`
   - Deploy

3. **Configuration**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

### Frontend Deployment (Vercel)

1. **Steps**
   - Push code to GitHub
   - Import project on Vercel
   - Set root directory to `frontend`
   - Configure build settings
   - Deploy

2. **Environment**
   - No build command needed (static files)
   - Output directory: `.`

### Database Setup (Supabase)

1. **Create Project**
   - Sign up at [supabase.com](https://supabase.com)
   - Create new project
   - Choose region closest to users

2. **Run SQL Schema**
   - Copy SQL from installation steps
   - Run in SQL Editor
   - Enable Row Level Security policies

3. **Get Credentials**
   - Project URL from Settings → API
   - Service role key (keep secret!)
   - Add to Render environment variables

**Live URLs:**
- Frontend: https://movie-review-smnz.vercel.app/
- Backend API: https://movie-review-fqp4.onrender.com
- Database: Supabase (managed PostgreSQL)

---

## 🤝 Contributing

Contributions are what make the open source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

**Ajinkya Wagh**

- Email: ajinkyawagh2005@gmail.com
- Phone: +91 8856875336
- GitHub: [@Ajinkyawagh4846](https://github.com/Ajinkyawagh4846)
- LinkedIn: [Ajinkya Wagh](https://www.linkedin.com/in/ajinkya-wagh-a201212b8/)

**Project Link**: [https://github.com/Ajinkyawagh4846/Movie-Review](https://github.com/Ajinkyawagh4846/Movie-Review)

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- [IMDb](https://www.imdb.com/) - Movie data source
- [TMDb](https://www.themoviedb.org/) - Movie posters and trailers
- [Supabase](https://supabase.com/) - PostgreSQL database and authentication
- [Scikit-learn](https://scikit-learn.org/) - Machine learning library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Vercel](https://vercel.com/) - Frontend hosting
- [Render](https://render.com/) - Backend hosting

---

<div align="center">

**Made with ❤️ by Ajinkya Wagh**

⭐ Star this repo if you find it helpful!

![GitHub stars](https://img.shields.io/github/stars/Ajinkyawagh4846/Movie-Review?style=social)
![GitHub forks](https://img.shields.io/github/forks/Ajinkyawagh4846/Movie-Review?style=social)

</div>
