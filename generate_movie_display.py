#!/usr/bin/env python3
"""
Enhanced Movie Reviews Static Display Generator - Generate beautiful HTML galleries from enhanced 
my_reviews.json using Jinja2 templates without Flask.

🖼️ STUNNING WEB DISPLAY FEATURES:
- 🎬 Beautiful movie card galleries with poster images
- 🌐 Language filtering with dedicated pages per language  
- 📱 Fully responsive design (desktop, tablet, mobile)
- ⭐ Star ratings with visual ★★★★★ display
- 🔗 Direct IMDb integration with clickable links
- 📊 Statistics dashboard (total movies, average rating, languages)
- 🎨 Modern gradient UI with hover effects and animations
- ⚡ Static HTML generation (no server required, works offline)

🌐 MULTI-LANGUAGE SUPPORT:
Automatically detects languages in your reviews and creates:
- index.html (all movies combined)
- index_hindi.html (Hindi movies only)
- index_english.html (English movies only)  
- index_[language].html (for each detected language)

📊 ENHANCED METADATA DISPLAY:
Each movie card shows:
- 🖼️ Movie poster image (with fallback placeholder)
- 📅 Year prominently displayed
- 🌐 Language badges prominently displayed
- 🎬 Director and genre information
- ⭐ Your rating + IMDb rating for reference
- 📝 Full review text with date
- 🔗 Clickable IMDb link with external icon

🎨 RESPONSIVE DESIGN:
- Grid layout adapts to screen size
- Mobile-optimized card layouts
- Touch-friendly navigation
- Beautiful gradient backgrounds
- Professional typography and spacing

🔄 BACKWARD COMPATIBILITY:
- Handles both legacy reviews (simple text) and enhanced reviews (rich metadata)
- Legacy reviews get special "Legacy" badges
- Graceful handling of missing poster images or metadata
- Smooth migration from old to new format

GENERATED FILES:
- movie_display/index.html - Main gallery with all movies
- movie_display/index_[language].html - Language-specific galleries
- Navigation links between all pages
- Statistics overview on each page

USAGE:
    python generate_movie_display.py

OUTPUT STRUCTURE:
    movie_display/
    ├── index.html                 # All movies gallery
    ├── index_hindi.html          # Hindi movies only
    ├── index_english.html        # English movies only
    ├── index_korean.html         # Korean movies only
    └── [additional languages]    # Based on your collection

TECHNICAL DETAILS:
- Pure Jinja2 templating (no Flask dependency)
- Static HTML generation for maximum compatibility
- Embedded CSS for self-contained files
- Font Awesome icons for professional look
- Optimized loading with efficient image handling

Author: Created for beautiful movie review visualization
Version: 2.0.0 - Enhanced with rich metadata and multi-language support
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader

# Configuration
REVIEWS_FILE = "my_reviews.json"
OUTPUT_DIR = "movie_display"
TEMPLATE_DIR = "templates"

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

def calculate_stats(movies: List[Dict[str, Any]], total_movies: int) -> Dict[str, Any]:
    """Calculate statistics for the movie collection."""
    total_rated = len([m for m in movies if isinstance(m["rating"], (int, float))])
    avg_rating = 0
    if total_rated > 0:
        rated_movies = [m for m in movies if isinstance(m["rating"], (int, float))]
        avg_rating = sum(m["rating"] for m in rated_movies) / len(rated_movies)
    
    return {
        "total_movies": total_movies,
        "total_rated": total_rated,
        "avg_rating": round(avg_rating, 1),
        "avg_stars": rating_to_stars(avg_rating)
    }

def generate_language_links(languages: List[str], current_language: str = "all") -> List[Dict[str, str]]:
    """Generate navigation links for language filtering."""
    links = [{"name": "All Languages", "file": "index.html", "active": current_language == "all"}]
    
    for lang in languages:
        safe_lang = lang.replace(" ", "_").replace(",", "").lower()
        links.append({
            "name": lang,
            "file": f"index_{safe_lang}.html",
            "active": current_language == lang
        })
    
    return links

def create_static_template() -> str:
    """Create the Jinja2 template as a string since we're not using Flask."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 My Movie Reviews{% if current_language != 'all' %} - {{ current_language }}{% endif %}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .stats {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            color: white;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .filters {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .filter-section {
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .filter-label {
            font-weight: bold;
            color: #333;
        }
        
        .language-links {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .language-link {
            padding: 8px 15px;
            border: 2px solid #ddd;
            border-radius: 20px;
            background: white;
            text-decoration: none;
            color: #333;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        .language-link:hover {
            border-color: #667eea;
            background: #667eea;
            color: white;
        }
        
        .language-link.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .movies-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .movie-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            position: relative;
        }
        
        .movie-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .movie-header {
            display: flex;
            padding: 20px;
            gap: 15px;
        }
        
        .movie-poster {
            width: 100px;
            height: 150px;
            border-radius: 10px;
            object-fit: cover;
            background: #f0f0f0;
        }
        
        .poster-placeholder {
            width: 100px;
            height: 150px;
            background: linear-gradient(45deg, #f0f0f0, #e0e0e0);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 12px;
            text-align: center;
            border-radius: 10px;
        }
        
        .movie-info {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        
        .movie-title {
            font-size: 1.4rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
            line-height: 1.2;
        }
        
        .movie-title a {
            color: #333;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .movie-title a:hover {
            color: #667eea;
        }
        
        .movie-meta {
            display: flex;
            flex-direction: column;
            gap: 5px;
            margin-bottom: 10px;
            font-size: 0.9rem;
            color: #666;
        }
        
        .rating-section {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .my-rating {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .stars {
            font-size: 1.1rem;
            color: #ffd700;
        }
        
        .imdb-rating {
            background: #f5c518;
            color: #000;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .movie-review {
            padding: 20px;
            background: #f8f9fa;
            border-top: 1px solid #eee;
        }
        
        .review-text {
            line-height: 1.6;
            color: #444;
            font-style: italic;
        }
        
        .review-date {
            margin-top: 10px;
            font-size: 0.8rem;
            color: #999;
            text-align: right;
        }
        
        .legacy-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #ff6b6b;
            color: white;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: bold;
        }
        
        .language-badge {
            display: inline-block;
            background: #e9ecef;
            color: #495057;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8rem;
            margin-right: 5px;
        }
        
        .no-movies {
            text-align: center;
            color: white;
            font-size: 1.2rem;
            margin: 50px 0;
        }
        
        .imdb-link {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            color: #f5c518;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: bold;
            transition: color 0.3s ease;
        }
        
        .imdb-link:hover {
            color: #e6b800;
        }
        
        @media (max-width: 768px) {
            .movies-grid {
                grid-template-columns: 1fr;
            }
            
            .movie-header {
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            
            .movie-info {
                align-items: center;
            }
            
            .filter-section {
                flex-direction: column;
                align-items: stretch;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 My Movie Reviews</h1>
            <p>Personal movie collection with ratings and reviews{% if current_language != 'all' %} - {{ current_language }}{% endif %}</p>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{{ stats.total_movies }}</div>
                <div>Total Movies</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ stats.total_rated }}</div>
                <div>Rated Movies</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ stats.avg_rating }}/10</div>
                <div>Average Rating {{ stats.avg_stars }}</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ languages|length }}</div>
                <div>Languages</div>
            </div>
        </div>
        
        <div class="filters">
            <div class="filter-section">
                <span class="filter-label">🌐 Filter by Language:</span>
                <div class="language-links">
                    {% for link in language_links %}
                    <a href="{{ link.file }}" class="language-link{% if link.active %} active{% endif %}">
                        {{ link.name }}
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        {% if movies %}
        <div class="movies-grid">
            {% for movie in movies %}
            <div class="movie-card">
                {% if movie.is_legacy %}
                <div class="legacy-badge">Legacy</div>
                {% endif %}
                
                <div class="movie-header">
                    {% if movie.poster_url %}
                    <img src="{{ movie.poster_url }}" alt="{{ movie.title }} Poster" class="movie-poster">
                    {% else %}
                    <div class="poster-placeholder">
                        <i class="fas fa-film" style="font-size: 2rem; margin-bottom: 5px;"></i>
                        <span>No Poster</span>
                    </div>
                    {% endif %}
                    
                    <div class="movie-info">
                        <h3 class="movie-title">
                            {% if movie.imdb_link %}
                            <a href="{{ movie.imdb_link }}" target="_blank" title="View on IMDb">
                                {{ movie.title }}
                                <i class="fas fa-external-link-alt" style="font-size: 0.8rem; color: #999;"></i>
                            </a>
                            {% else %}
                            {{ movie.title }}
                            {% endif %}
                        </h3>
                        
                        <div class="movie-meta">
                            {% if movie.year != "Unknown" %}
                            <span><strong>📅 Year:</strong> {{ movie.year }}</span>
                            {% endif %}
                            {% if movie.director != "Unknown" %}
                            <span><strong>🎬 Director:</strong> {{ movie.director }}</span>
                            {% endif %}
                            {% if movie.genre != "Unknown" %}
                            <span><strong>🎭 Genre:</strong> {{ movie.genre }}</span>
                            {% endif %}
                        </div>
                        
                        <div class="rating-section">
                            {% if movie.rating != "N/A" %}
                            <span class="my-rating">{{ movie.rating }}/10</span>
                            <span class="stars">{{ movie.stars }}</span>
                            {% endif %}
                            {% if movie.imdb_rating != "N/A" %}
                            <span class="imdb-rating">IMDb {{ movie.imdb_rating }}</span>
                            {% endif %}
                        </div>
                        
                        {% if movie.language != "Unknown" %}
                        <div style="margin-top: 5px;">
                            {% set languages = movie.language.split(',') %}
                            {% for lang in languages %}
                            <span class="language-badge">{{ lang.strip() }}</span>
                            {% endfor %}
                        </div>
                        {% endif %}
                        
                        {% if movie.imdb_link %}
                        <div style="margin-top: 10px;">
                            <a href="{{ movie.imdb_link }}" target="_blank" class="imdb-link">
                                <i class="fab fa-imdb"></i>
                                View on IMDb
                            </a>
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="movie-review">
                    <div class="review-text">"{{ movie.review }}"</div>
                    <div class="review-date">Reviewed on {{ movie.date_added }}</div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="no-movies">
            <p>No movies found for the selected language filter.</p>
        </div>
        {% endif %}
    </div>
</body>
</html>"""

def generate_html_files():
    """Generate static HTML files for all movies and language filters."""
    print("🎬 Loading movie reviews...")
    reviews = load_reviews()
    
    if not reviews:
        print("❌ No reviews found in my_reviews.json")
        return
    
    print(f"📚 Found {len(reviews)} movie reviews")
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    # Setup Jinja2 environment with string template
    template_str = create_static_template()
    env = Environment()
    template = env.from_string(template_str)
    
    # Get all languages
    languages = get_languages(reviews)
    print(f"🌐 Found languages: {', '.join(languages)}")
    
    # Generate main page (all movies)
    print("📄 Generating index.html (all movies)...")
    all_movies = prepare_movie_data(reviews)
    stats = calculate_stats(all_movies, len(reviews))
    language_links = generate_language_links(languages, "all")
    
    html_content = template.render(
        movies=all_movies,
        languages=languages,
        stats=stats,
        language_links=language_links,
        current_language="all"
    )
    
    with open(f"{OUTPUT_DIR}/index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Generate filtered pages for each language
    for language in languages:
        safe_lang = language.replace(" ", "_").replace(",", "").lower()
        filename = f"index_{safe_lang}.html"
        print(f"📄 Generating {filename} ({language} movies)...")
        
        filtered_movies = prepare_movie_data(reviews, language)
        filtered_stats = calculate_stats(filtered_movies, len(reviews))
        language_links = generate_language_links(languages, language)
        
        html_content = template.render(
            movies=filtered_movies,
            languages=languages,
            stats=filtered_stats,
            language_links=language_links,
            current_language=language
        )
        
        with open(f"{OUTPUT_DIR}/{filename}", 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    print(f"\n✅ HTML files generated successfully!")
    print(f"📁 Output directory: {OUTPUT_DIR}/")
    print(f"🌐 Open {OUTPUT_DIR}/index.html in your browser to view all movies")
    print(f"🎯 Language-specific pages: {len(languages)} files generated")

if __name__ == '__main__':
    generate_html_files() 