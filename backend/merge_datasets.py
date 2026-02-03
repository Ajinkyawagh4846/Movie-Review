import pandas as pd
import os
import numpy as np

# Get paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, 'data')

print("="*70)
print("MERGING DATASETS")
print("="*70)

# Load existing movies
existing_movies = pd.read_csv(os.path.join(data_dir, 'imdb_list.csv'))
print(f"\n✅ Existing movies: {len(existing_movies)}")

# Load new Indian movies
indian_movies = pd.read_csv(os.path.join(data_dir, 'movie_data_all3.csv'))
print(f"✅ New Indian movies dataset: {len(indian_movies)}")

# Clean and prepare Indian movies
indian_clean = indian_movies[['Title', 'Year', 'IMDb Rating', 'Genre']].copy()

# Remove rows with missing data
indian_clean = indian_clean.dropna(subset=['Title', 'IMDb Rating'])

# Remove rows where rating is 'N/A' or not numeric
indian_clean = indian_clean[pd.to_numeric(indian_clean['IMDb Rating'], errors='coerce').notna()]
indian_clean['IMDb Rating'] = pd.to_numeric(indian_clean['IMDb Rating'], errors='coerce')

# Rename columns to match existing format
indian_clean = indian_clean.rename(columns={
    'Title': 'title',
    'Year': 'year',
    'IMDb Rating': 'rating',
    'Genre': 'genre'
})

# Convert year to integer
indian_clean['year'] = indian_clean['year'].astype(str).str[:4]
indian_clean['year'] = pd.to_numeric(indian_clean['year'], errors='coerce')

# Remove NaN values
indian_clean = indian_clean.dropna(subset=['year', 'rating'])

# Fill NaN in genre with "Not Available"
indian_clean['genre'] = indian_clean['genre'].fillna('Not Available')

# Filter: Only movies with rating >= 5 and year >= 2000
indian_clean = indian_clean[
    (indian_clean['rating'] >= 5.0) & 
    (indian_clean['year'] >= 2000) &
    (indian_clean['year'] <= 2024)
]

# Create unique IDs for Indian movies
indian_clean['id'] = 'ind_' + indian_clean.reset_index(drop=True).index.astype(str).str.zfill(6)

# Add flags
indian_clean['has_reviews'] = False
indian_clean['poster_url'] = None

print(f"✅ After filtering: {len(indian_clean)} Indian movies (rating ≥5, year 2000-2024)")

# Add flag to existing movies
existing_movies['has_reviews'] = True
if 'poster_url' not in existing_movies.columns:
    existing_movies['poster_url'] = None

# Combine datasets
combined = pd.concat([existing_movies, indian_clean], ignore_index=True)

# Remove duplicates
combined = combined.drop_duplicates(subset=['title'], keep='first')

# Final cleanup - ensure no NaN values
combined['genre'] = combined['genre'].fillna('Not Available')
combined['year'] = combined['year'].fillna(2000).astype(int)
combined['rating'] = combined['rating'].fillna(5.0).astype(float)

print(f"\n✅ Total combined movies: {len(combined)}")
print(f"   - With sentiment analysis: {combined['has_reviews'].sum()}")
print(f"   - Info only (no reviews): {(~combined['has_reviews']).sum()}")

# Save combined dataset
output_path = os.path.join(data_dir, 'imdb_list_combined.csv')
combined.to_csv(output_path, index=False)

print(f"\n✅ Saved to: imdb_list_combined.csv")
print("="*70)