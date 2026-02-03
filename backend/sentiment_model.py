import pandas as pd
import numpy as np
import os
import re
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Download required NLTK data
print("Downloading NLTK data...")
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class SentimentAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = MultinomialNB()
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text):
        """Clean and preprocess review text"""
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def prepare_data(self, reviews_df):
        """Prepare data for training"""
        print("\nPreparing data...")
        
        # Clean review text
        reviews_df['cleaned_review'] = reviews_df['review'].apply(self.clean_text)
        
        # Create sentiment labels based on ratings
        # 1-4: Negative (0), 5-7: Neutral (1), 8-10: Positive (2)
        def get_sentiment(rating):
            if rating <= 4:
                return 0  # Negative
            elif rating <= 7:
                return 1  # Neutral
            else:
                return 2  # Positive
        
        reviews_df['sentiment'] = reviews_df['review_rating'].apply(get_sentiment)
        
        print(f"Total reviews: {len(reviews_df)}")
        print(f"\nSentiment distribution:")
        print(f"Negative (0): {(reviews_df['sentiment'] == 0).sum()}")
        print(f"Neutral (1): {(reviews_df['sentiment'] == 1).sum()}")
        print(f"Positive (2): {(reviews_df['sentiment'] == 2).sum()}")
        
        return reviews_df
    
    def train(self, reviews_df):
        """Train the sentiment analysis model"""
        print("\n" + "="*70)
        print("TRAINING SENTIMENT ANALYSIS MODEL")
        print("="*70)
        
        # Prepare data
        reviews_df = self.prepare_data(reviews_df)
        
        # Split data
        X = reviews_df['cleaned_review']
        y = reviews_df['sentiment']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nTraining set size: {len(X_train)}")
        print(f"Test set size: {len(X_test)}")
        
        # Vectorize text
        print("\nVectorizing text...")
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train model
        print("Training model...")
        self.model.fit(X_train_vec, y_train)
        
        # Evaluate
        print("\nEvaluating model...")
        y_pred = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['Negative', 'Neutral', 'Positive']))
        
        return accuracy
    
    def predict_sentiment(self, review_text):
        """Predict sentiment for a single review"""
        cleaned = self.clean_text(review_text)
        vectorized = self.vectorizer.transform([cleaned])
        prediction = self.model.predict(vectorized)[0]
        probability = self.model.predict_proba(vectorized)[0]
        
        return {
            'sentiment': int(prediction),
            'sentiment_label': ['Negative', 'Neutral', 'Positive'][prediction],
            'confidence': float(probability[prediction])
        }
    
    def save_model(self, model_path='../models/sentiment_model.pkl'):
        """Save trained model"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        full_path = os.path.join(project_dir, 'models', 'sentiment_model.pkl')
        
        joblib.dump({
            'vectorizer': self.vectorizer,
            'model': self.model
        }, full_path)
        print(f"\n✅ Model saved to: {full_path}")
    
    def load_model(self, model_path='../models/sentiment_model.pkl'):
        """Load trained model"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        full_path = os.path.join(project_dir, 'models', 'sentiment_model.pkl')
        
        saved_data = joblib.load(full_path)
        self.vectorizer = saved_data['vectorizer']
        self.model = saved_data['model']
        print(f"✅ Model loaded from: {full_path}")


# Main training script
if __name__ == "__main__":
    # Load data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, 'data')
    
    print("Loading reviews dataset...")
    reviews_df = pd.read_csv(os.path.join(data_dir, 'imdb_reviews.csv'))
    
    # Train model
    analyzer = SentimentAnalyzer()
    accuracy = analyzer.train(reviews_df)
    
    # Save model
    analyzer.save_model()
    
    # Test prediction
    print("\n" + "="*70)
    print("TESTING MODEL WITH SAMPLE REVIEWS")
    print("="*70)
    
    sample_positive = reviews_df[reviews_df['review_rating'] >= 9].iloc[0]['review']
    sample_negative = reviews_df[reviews_df['review_rating'] <= 3].iloc[0]['review']
    
    print("\n--- Testing Positive Review ---")
    print(f"Original text: {sample_positive[:200]}...")
    result = analyzer.predict_sentiment(sample_positive)
    print(f"Prediction: {result['sentiment_label']} (Confidence: {result['confidence']:.2%})")
    
    print("\n--- Testing Negative Review ---")
    print(f"Original text: {sample_negative[:200]}...")
    result = analyzer.predict_sentiment(sample_negative)
    print(f"Prediction: {result['sentiment_label']} (Confidence: {result['confidence']:.2%})")
    
    print("\n" + "="*70)
    print("✅ MODEL TRAINING COMPLETE!")
    print("="*70)