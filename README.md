# 🎬 FilmReviewer - AI-Powered Movie Sentiment Analysis

<div align="center">

![FilmReviewer](https://img.shields.io/badge/FilmReviewer-AI%20Powered-blueviolet)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.0-green)
![Machine Learning](https://img.shields.io/badge/ML-Sentiment%20Analysis-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Discover what people really think about your favorite movies through advanced AI sentiment analysis**

[Live Demo](movie-reviewer-two.vercel.app) • [Live Backend](https://movie-reviewer-9nhp.onrender.com) • [Report Bug](https://github.com/Ajinkyawagh4846/movie-reviewer) • [Request Feature](https://github.com/Ajinkyawagh4846/movie-reviewer)

</div>

---

## 🎯 About The Project

**FilmReviewer** is an intelligent movie sentiment analysis platform that helps users make informed viewing decisions by analyzing thousands of movie reviews using advanced Natural Language Processing (NLP) and Machine Learning techniques.

### Why FilmReviewer?

- 🤖 **AI-Powered Analysis**: Uses ML models trained on 6,241+ real movie reviews
- 📊 **Comprehensive Insights**: Get detailed sentiment breakdowns (Positive, Neutral, Negative)
- 🎭 **Large Database**: Browse 249+ movies with full sentiment analysis, and 800+ movies with ratings.
- 🔐 **User Features**: Account system with search history and personalized recommendations
- 🌙 **Modern UI**: Beautiful, responsive interface with dark mode support
- 🚀 **Fast & Reliable**: Cached API responses for instant results

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
- 💾 **Data Persistence** - SQLite database for user data
- ⚡ **API Caching** - Fast response times with intelligent caching
- 🔒 **Secure Authentication** - Password hashing with SHA-256

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

### 🔹 Machine Learning, NLP & DB
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikitlearn)
![NLTK](https://img.shields.io/badge/NLTK-NLP-green)
![TF--IDF](https://img.shields.io/badge/TF--IDF-Vectorization-blueviolet)
![Naive Bayes](https://img.shields.io/badge/Naive%20Bayes-Classifier-red)
![Text Preprocessing](https://img.shields.io/badge/Text-Preprocessing-lightgrey)
![SQLite](https://img.shields.io/badge/SQLite-Local%20DB-blue?logo=sqlite)

### 🔹 APIs & External Services
![TMDb API](https://img.shields.io/badge/TMDb-Movie%20API-01B4E4)
![Fetch API](https://img.shields.io/badge/Fetch-API-green)

### 🔹 Deployment & Editors
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

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/filmreviewer.git
   cd filmreviewer
```

2. **Set up the backend**
```bash
   cd backend
   pip install -r requirements.txt
```

3. **Download NLTK data** (first time only)
```python
   python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

4. **Train the ML model** (if not already trained)
```bash
   python sentiment_model.py
```

5. **Start the backend server**
```bash
   python app.py
```

6. **Open the frontend**
   - Navigate to `frontend/index.html` in your browser
   - Or use Live Server extension in VS Code

7. **Access the application**
   - Frontend: `http://127.0.0.1:5500`
   - Backend API: `http://127.0.0.1:5000`

---

## 📖 Usage

### For Users

1. **Browse Movies** - Explore 1047+ movies with filters
2. **Search** - Type movie name and get instant suggestions
3. **Analyze** - Click on any movie to see sentiment analysis
4. **Create Account** - Sign up to save search history
5. **Submit Reviews** - Share your opinions with the community

### For Developers
```python
# Example: Using the sentiment analysis API
import requests

response = requests.get('http://127.0.0.1:5000/api/analyze/tt1431045')
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
│   ├── database.py             # Database operations
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
├── users.db                   # SQLite database
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

### Data Preprocessing
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
Production: https://filmreviewer-api.onrender.com
Development: http://127.0.0.1:5000
```

### Endpoints

#### Get All Movies
```http
GET /api/movies
```
Returns list of all movies

#### Search Movies
```http
GET /api/search?q=Deadpool
```

#### Analyze Movie
```http
GET /api/analyze/{movie_id}
```

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

---

## 🌐 Deployment

### Backend (Render)
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set environment variables
5. Deploy

### Frontend (Vercel)
1. Push code to GitHub
2. Import project on Vercel
3. Configure build settings
4. Deploy

**Live URLs:**
- Frontend: https://filmreviewer.vercel.app
- Backend API: https://filmreviewer-api.onrender.com

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
- GitHub: https://github.com/Ajinkyawagh4846
- LinkedIn: https://www.linkedin.com/in/ajinkya-wagh-a201212b8/

**Project Link**: https://github.com/Ajinkyawagh4846/movie-reviewer

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- [IMDb](https://www.imdb.com/) - Movie data source
- [TMDb](https://www.themoviedb.org/) - Movie posters and trailers
- [Scikit-learn](https://scikit-learn.org/) - Machine learning library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Vercel](https://vercel.com/) - Frontend hosting
- [Render](https://render.com/) - Backend hosting

---

<div align="center">

**Made with ❤️ by Ajinkya Wagh**

⭐ Star this repo if you find it helpful!

</div>
