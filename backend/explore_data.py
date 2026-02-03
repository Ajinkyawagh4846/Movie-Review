import pandas as pd
import numpy as np
import os

# Get the correct path to data folder
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, 'data')

# Load the datasets
movies_df = pd.read_csv(os.path.join(data_dir, 'imdb_list.csv'))
reviews_df = pd.read_csv(os.path.join(data_dir, 'imdb_reviews.csv'))

print("="*70)
print("MOVIE DATASET EXPLORATION")
print("="*70)

print(f"\nTotal Movies: {len(movies_df)}")
print(f"\nFirst 5 Movies:")
print(movies_df.head())

print("\n" + "="*70)
print("REVIEWS DATASET EXPLORATION")
print("="*70)

print(f"\nTotal Reviews: {len(reviews_df)}")
print(f"\nColumns: {reviews_df.columns.tolist()}")
print(f"\nUnique Movies with Reviews: {reviews_df['imdb_id'].nunique()}")
print(f"\nAverage Reviews per Movie: {len(reviews_df) / reviews_df['imdb_id'].nunique():.1f}")

print("\n" + "="*70)
print("REVIEW RATINGS DISTRIBUTION")
print("="*70)
print(reviews_df['review_rating'].value_counts().sort_index())

print("\n" + "="*70)
print("SAMPLE REVIEWS")
print("="*70)

# Show one positive and one negative review
positive_review = reviews_df[reviews_df['review_rating'] >= 8].iloc[0]
negative_review = reviews_df[reviews_df['review_rating'] <= 4].iloc[0]

print("\n--- POSITIVE REVIEW (Rating: {}) ---".format(positive_review['review_rating']))
print(f"Title: {positive_review['review title']}")
print(f"Review: {positive_review['review'][:300]}...")

print("\n--- NEGATIVE REVIEW (Rating: {}) ---".format(negative_review['review_rating']))
print(f"Title: {negative_review['review title']}")
print(f"Review: {negative_review['review'][:300]}...")

print("\n" + "="*70)
print("TOP 5 MOVIES BY NUMBER OF REVIEWS")
print("="*70)

top_movies = reviews_df['imdb_id'].value_counts().head(5)
for imdb_id, count in top_movies.items():
    movie_name = movies_df[movies_df['id'] == imdb_id]['title'].values
    if len(movie_name) > 0:
        print(f"{movie_name[0]}: {count} reviews")