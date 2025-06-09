#!/usr/bin/env python3
"""
Movie Reviews Display - A web interface to display your movie reviews
from my_reviews.json with beautiful formatting, language filtering, and IMDb integration.

Features:
- Beautiful card-based layout for each movie
- Filter movies by language
- Display movie posters
- Direct links to IMDb pages
- Star ratings and review text
- Responsive design

Author: Created for personal movie review display
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from typing import Dict, List, Any

app = Flask(__name__)

# Configuration
REVIEWS_FILE = "my_reviews.json"

def load_reviews() -> Dict[str, Any]:
    """Load movie reviews from JSON file."""
    try:
        if os.path.exists(REVIEWS_FILE):
            with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading reviews: {e}")
        return {}

def rating_to_stars(rating) -> str:
    """Convert numeric rating to star representation."""
    if not isinstance(rating, (int, float)):
        return "☆☆☆☆☆"
    
    full_stars = int(rating // 2)
    half_star = 1 if (rating % 2) >= 1 else 0
    empty_stars = 5 - full_stars - half_star
    
    return "★" * full_stars + ("☆" if half_star else "") + "☆" * empty_stars

def format_date(date_string: str) -> str:
    """Format date string for display."""
    try:
        if not date_string or date_string == "Unknown":
            return "Unknown"
        # Parse ISO format and return readable date
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_string

def get_languages(reviews: Dict[str, Any]) -> List[str]:
    """Extract unique languages from reviews for filtering."""
    languages = set()
    
    for review_data in reviews.values():
        if isinstance(review_data, dict):
            language = review_data.get("language", "")
            if language:
                # Split multiple languages and add each one
                for lang in language.split(","):
                    lang = lang.strip()
                    if lang and lang != "N/A":
                        languages.add(lang)
    
    return sorted(list(languages))

def prepare_movie_data(reviews: Dict[str, Any], language_filter: str = None) -> List[Dict[str, Any]]:
    """Prepare movie data for template display."""
    movies = []
    
    for title, review_data in reviews.items():
        # Handle both legacy format (string) and new format (dict)
        if isinstance(review_data, str):
            movie = {
                "title": title,
                "rating": "N/A",
                "stars": "☆☆☆☆☆",
                "review": review_data,
                "date_added": "Unknown",
                "poster_url": None,
                "imdb_link": None,
                "year": "Unknown",
                "director": "Unknown",
                "genre": "Unknown",
                "language": "Unknown",
                "country": "Unknown",
                "imdb_rating": "N/A",
                "is_legacy": True
            }
        else:
            movie = {
                "title": title,
                "rating": review_data.get("rating", "N/A"),
                "stars": rating_to_stars(review_data.get("rating", 0)),
                "review": review_data.get("review", "No review"),
                "date_added": format_date(review_data.get("date_added", "Unknown")),
                "poster_url": review_data.get("poster_url", None),
                "imdb_link": review_data.get("imdb_link", None),
                "year": review_data.get("year", "Unknown"),
                "director": review_data.get("director", "Unknown"),
                "genre": review_data.get("genre", "Unknown"),
                "language": review_data.get("language", "Unknown"),
                "country": review_data.get("country", "Unknown"),
                "imdb_rating": review_data.get("imdb_rating", "N/A"),
                "is_legacy": False
            }
        
        # Apply language filter if specified
        if language_filter and language_filter != "all":
            movie_language = movie["language"].lower()
            if language_filter.lower() not in movie_language:
                continue
        
        movies.append(movie)
    
    # Sort movies by rating (highest first), then by title
    def sort_key(movie):
        rating = movie["rating"]
        if isinstance(rating, (int, float)):
            return (-rating, movie["title"])
        else:
            return (-999, movie["title"])  # Legacy reviews go to bottom
    
    movies.sort(key=sort_key)
    return movies

@app.route('/')
def index():
    """Main page displaying all movie reviews."""
    reviews = load_reviews()
    languages = get_languages(reviews)
    language_filter = request.args.get('language', 'all')
    
    movies = prepare_movie_data(reviews, language_filter if language_filter != 'all' else None)
    
    # Calculate statistics
    total_movies = len(reviews)
    total_rated = len([m for m in movies if isinstance(m["rating"], (int, float))])
    avg_rating = 0
    if total_rated > 0:
        rated_movies = [m for m in movies if isinstance(m["rating"], (int, float))]
        avg_rating = sum(m["rating"] for m in rated_movies) / len(rated_movies)
    
    stats = {
        "total_movies": total_movies,
        "total_rated": total_rated,
        "avg_rating": round(avg_rating, 1),
        "avg_stars": rating_to_stars(avg_rating)
    }
    
    return render_template('movie_reviews.html', 
                         movies=movies, 
                         languages=languages,
                         selected_language=language_filter,
                         stats=stats)

@app.route('/api/movies')
def api_movies():
    """API endpoint for getting movie data."""
    reviews = load_reviews()
    language_filter = request.args.get('language')
    movies = prepare_movie_data(reviews, language_filter if language_filter != 'all' else None)
    return jsonify(movies)

if __name__ == '__main__':
    print("🎬 Starting Movie Reviews Display Server...")
    print("📁 Reviews file:", REVIEWS_FILE)
    print("🌐 Open http://localhost:5000 in your browser")
    print("🎭 Features: Language filtering, IMDb links, movie posters")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 