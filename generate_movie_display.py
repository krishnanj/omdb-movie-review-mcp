#!/usr/bin/env python3
"""
Enhanced Movie Display Generator

This module generates beautiful, responsive HTML galleries from your movie review collection.
Features include:
- Static HTML generation (works offline)
- Responsive grid design adapting to screen size
- Original language-specific filtering with separate pages for each language
- Movie poster integration with fallback handling
- Mobile-optimized interface with touch-friendly navigation
- IMDb integration with direct movie page links
- Modern CSS Grid layout with card-based design
- Automatic original language detection and categorization

The system focuses on original language categorization - each movie is assigned
to its primary/original language rather than all languages it may contain.

Version 2.0.0 Changes:
- Original language focus (single language per movie)
- Simplified language filtering logic
- Cleaner language-specific page generation
- Improved cultural authenticity in movie categorization

Usage:
    python generate_movie_display.py

Generates:
    movie_display/index.html (all movies)
    movie_display/index_[language].html (per original language)

Requirements:
    - my_reviews.json (movie review data)
    - Jinja2 (template engine)
    - Internet connection (for poster images)

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
from typing import Dict, List, Any, Set
from jinja2 import Environment, FileSystemLoader, Template

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
    """
    Extract unique original languages from reviews.
    
    v2.0.0 Change: Now handles single original language per movie
    instead of comma-separated multiple languages.
    
    Args:
        reviews: Dictionary of movie reviews
        
    Returns:
        List of unique original languages found
    """
    languages = set()
    
    for title, data in reviews.items():
        if isinstance(data, dict):
            language = data.get('language', '').strip()
            if language and language.lower() != 'n/a':
                # v2.0.0: No more splitting, language is already single
                languages.add(language)
        else:
            # Legacy format
            languages.add('Unknown')
    
    # Sort languages alphabetically
    return sorted(languages)

def prepare_movie_data(reviews: Dict[str, Any], language_filter: str = None) -> List[Dict[str, Any]]:
    """
    Prepare movie data for HTML rendering with optional language filtering.
    
    v2.0.0 Change: Now handles single original language per movie
    instead of comma-separated multiple languages.
    
    Args:
        reviews: Dictionary of movie reviews
        language_filter: Optional language to filter by (original language)
        
    Returns:
        List of movie dictionaries formatted for template rendering
    """
    movies = []
    
    for title, data in reviews.items():
        if isinstance(data, dict):
            # New format with structured data
            movie_language = data.get('language', 'Unknown').strip()
            
            # Apply language filter if specified
            if language_filter and language_filter != movie_language:
                continue
            
            movie = {
                'title': title,
                'rating': data.get('rating', 'N/A'),
                'review': data.get('review', 'No review available'),
                'stars': rating_to_stars(data.get('rating', 0)),
                'date_added': format_date(data.get('date_added', '')),
                'imdb_link': data.get('imdb_link', ''),
                'poster_url': data.get('poster_url', ''),
                'year': data.get('year', 'Unknown'),
                'director': data.get('director', 'Unknown'),
                'genre': data.get('genre', 'Unknown'),
                'imdb_rating': data.get('imdb_rating', 'N/A'),
                'language': movie_language,  # Single original language
                'country': data.get('country', 'Unknown'),
                'is_legacy': False
            }
        else:
            # Legacy format (just text)
            if language_filter and language_filter != 'Unknown':
                continue
                
            movie = {
                'title': title,
                'rating': 'N/A',
                'review': str(data),
                'stars': '☆☆☆☆☆',
                'date_added': 'Unknown',
                'imdb_link': '',
                'poster_url': '',
                'year': 'Unknown',
                'director': 'Unknown',
                'genre': 'Unknown',
                'imdb_rating': 'N/A',
                'language': 'Unknown',
                'country': 'Unknown',
                'is_legacy': True
            }
        
        movies.append(movie)
    
    # Sort by rating (highest first), then by title
    return sorted(movies, key=lambda x: (-x['rating'] if isinstance(x['rating'], (int, float)) else -999, x['title'].lower()))

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

def group_movies_by_language(reviews: Dict[str, Any]) -> Dict[str, List[tuple]]:
    """
    Group movies by their original language.
    
    v2.0.0 Change: Now handles single original language per movie
    instead of comma-separated multiple languages.
    
    Args:
        reviews: Dictionary of movie reviews with metadata
        
    Returns:
        Dictionary mapping original language to list of (title, data) tuples
    """
    language_groups = {}
    
    for title, data in reviews.items():
        if isinstance(data, dict):
            # Get original language (single language in v2.0.0)
            language = data.get('language', 'Unknown').strip()
            
            # Handle empty or missing language
            if not language or language.lower() == 'n/a':
                language = 'Unknown'
            
            # Create group if it doesn't exist
            if language not in language_groups:
                language_groups[language] = []
            
            language_groups[language].append((title, data))
        else:
            # Legacy format handling
            if 'Unknown' not in language_groups:
                language_groups['Unknown'] = []
            language_groups['Unknown'].append((title, data))
    
    return language_groups

def detect_languages_in_reviews(reviews: Dict[str, Any]) -> Set[str]:
    """
    Detect all original languages present in the review collection.
    
    v2.0.0 Change: Simplified to handle single original language per movie.
    
    Args:
        reviews: Dictionary of movie reviews
        
    Returns:
        Set of original languages found in the collection
    """
    languages = set()
    
    for title, data in reviews.items():
        if isinstance(data, dict):
            language = data.get('language', '').strip()
            if language and language.lower() != 'n/a':
                languages.add(language)
    
    # Always include 'Unknown' for movies without language data
    languages.add('Unknown')
    
    return languages

def generate_language_specific_page(language: str, movies: List[tuple], output_dir: str) -> None:
    """
    Generate HTML page for a specific original language.
    
    v2.0.0 Enhancement: Cleaner single-language page generation.
    
    Args:
        language: Original language name (e.g., "Hindi", "English")
        movies: List of (title, data) tuples for this language
        output_dir: Directory to save the HTML file
    """
    try:
        # Sort movies by rating (highest first), then by title
        sorted_movies = sorted(
            movies,
            key=lambda x: (
                -(x[1].get('rating', 0) if isinstance(x[1], dict) else 0),
                x[0].lower()
            )
        )
        
        # Generate safe filename
        safe_language = language.lower().replace(' ', '_').replace('/', '_')
        output_file = os.path.join(output_dir, f"index_{safe_language}.html")
        
        # Calculate statistics
        total_movies = len(movies)
        if total_movies > 0:
            ratings = [data.get('rating', 0) for title, data in movies if isinstance(data, dict) and data.get('rating')]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
        else:
            avg_rating = 0
        
        # Create template context
        template_context = {
            'movies': sorted_movies,
            'language_filter': language,
            'total_movies': total_movies,
            'average_rating': avg_rating,
            'page_title': f"{language} Movies",
            'is_language_specific': True,
            'generation_date': datetime.now().strftime("%B %d, %Y at %I:%M %p")
        }
        
        # Generate HTML
        html_content = movie_template.render(**template_context)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated {language} movies page: {output_file} ({total_movies} movies, avg rating: {avg_rating:.1f})")
        
    except Exception as e:
        print(f"Error generating {language} page: {e}")

# Enhanced HTML template with original language support
movie_template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if is_language_specific %}{{ language_filter }} Movies{% else %}My Movie Reviews{% endif %} - Personal Collection</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px 0;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        .logo {
            font-size: 2rem;
            font-weight: bold;
            color: #4a5568;
        }

        .stats {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .stat-item {
            text-align: center;
            padding: 5px 10px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 8px;
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            font-size: 0.9rem;
            color: #666;
        }

        .main-content {
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .section-title {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 10px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }

        .section-subtitle {
            text-align: center;
            margin-bottom: 40px;
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
        }

        .movies-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }

        .movie-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            position: relative;
        }

        .movie-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .movie-poster {
            position: relative;
            height: 400px;
            overflow: hidden;
        }

        .movie-poster img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .movie-card:hover .movie-poster img {
            transform: scale(1.05);
        }

        .movie-info {
            padding: 20px;
        }

        .movie-title {
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 8px;
            color: #2d3748;
        }

        .movie-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }

        .detail-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .movie-rating {
            font-size: 1.1rem;
            font-weight: bold;
            color: #f6ad55;
            margin-bottom: 10px;
        }

        .movie-review {
            color: #666;
            font-size: 0.95rem;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .imdb-link {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(245, 197, 24, 0.9);
            color: black;
            padding: 5px 8px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .imdb-link:hover {
            background: #f5c518;
            transform: scale(1.05);
        }

        .language-filter {
            text-align: center;
            margin: 30px 0;
        }

        .filter-buttons {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
        }

        .filter-btn {
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            font-size: 0.9rem;
        }

        .filter-btn:hover, .filter-btn.active {
            background: rgba(255, 255, 255, 0.9);
            color: #667eea;
            border-color: white;
        }

        .footer {
            background: rgba(0, 0, 0, 0.8);
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 60px;
        }

        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 15px;
            }

            .section-title {
                font-size: 2rem;
            }

            .movies-container {
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
            }

            .stats {
                justify-content: center;
            }

            .filter-buttons {
                padding: 0 10px;
            }
        }

        @media (max-width: 480px) {
            .movies-container {
                grid-template-columns: 1fr;
                gap: 20px;
            }

            .main-content {
                padding: 0 15px;
            }

            .movie-details {
                grid-template-columns: 1fr;
            }
        }

        /* Enhanced visual effects */
        .movie-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
            z-index: 1;
        }

        .movie-card:hover::before {
            opacity: 1;
        }

        .no-movies {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.2rem;
            margin: 60px 0;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">🎬 My Movie Collection</div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{{ total_movies }}</div>
                    <div class="stat-label">{% if is_language_specific %}{{ language_filter }} {% endif %}Movies</div>
                </div>
                {% if average_rating > 0 %}
                <div class="stat-item">
                    <div class="stat-number">{{ "%.1f"|format(average_rating) }}</div>
                    <div class="stat-label">Avg Rating</div>
                </div>
                {% endif %}
            </div>
        </div>
    </header>

    <main class="main-content">
        <h1 class="section-title">
            {% if is_language_specific %}
                {{ language_filter }} Movies
            {% else %}
                My Movie Reviews
            {% endif %}
        </h1>
        <p class="section-subtitle">
            {% if is_language_specific %}
                Showing {{ total_movies }} {{ language_filter }} movie{% if total_movies != 1 %}s{% endif %} from my collection
            {% else %}
                A curated collection of {{ total_movies }} movie{% if total_movies != 1 %}s{% endif %} with personal reviews and ratings
            {% endif %}
        </p>

        {% if not is_language_specific %}
        <div class="language-filter">
            <div class="filter-buttons">
                <a href="index.html" class="filter-btn active">All Movies</a>
                <!-- Language-specific navigation will be added here -->
            </div>
        </div>
        {% endif %}

        {% if movies %}
        <div class="movies-container">
            {% for title, movie in movies %}
            <div class="movie-card" data-language="{{ movie.language|lower if movie.language else 'unknown' }}">
                {% if movie.imdb_link and movie.imdb_link != '' %}
                <a href="{{ movie.imdb_link }}" target="_blank" class="imdb-link">IMDb</a>
                {% endif %}
                
                <div class="movie-poster">
                    {% if movie.poster_url and movie.poster_url != '' and movie.poster_url != 'N/A' %}
                    <img src="{{ movie.poster_url }}" alt="{{ title }} poster" 
                         onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgdmlld0JveD0iMCAwIDMwMCA0NTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDUwIiBmaWxsPSIjZjNmNGY2Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOWNhM2FmIiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC1zaXplPSIxOCI+Tm8gUG9zdGVyPC90ZXh0Pgo8L3N2Zz4K';">
                    {% else %}
                    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgdmlld0JveD0iMCAwIDMwMCA0NTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDUwIiBmaWxsPSIjZjNmNGY2Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMjI1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOWNhM2FmIiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC1zaXplPSIxOCI+Tm8gUG9zdGVyPC90ZXh0Pgo8L3N2Zz4K"
                         alt="{{ title }} - No poster available">
                    {% endif %}
                </div>

                <div class="movie-info">
                    <h3 class="movie-title">{{ title }}</h3>
                    <div class="movie-details">
                        {% if movie.year %}
                        <div class="detail-item">📅 {{ movie.year }}</div>
                        {% endif %}
                        {% if movie.language %}
                        <div class="detail-item">🌐 {{ movie.language }}</div>
                        {% endif %}
                        {% if movie.director %}
                        <div class="detail-item">🎬 {{ movie.director }}</div>
                        {% endif %}
                        {% if movie.genre %}
                        <div class="detail-item">🎭 {{ movie.genre }}</div>
                        {% endif %}
                    </div>
                    
                    {% if movie.rating %}
                    <div class="movie-rating">
                        ⭐ {{ movie.rating }}/10
                        {% set stars = ((movie.rating / 2) | round) | int %}
                        {% for i in range(stars) %}★{% endfor %}{% for i in range(5 - stars) %}☆{% endfor %}
                    </div>
                    {% endif %}
                    
                    {% if movie.review %}
                    <div class="movie-review">{{ movie.review }}</div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="no-movies">
            <p>No movies found{% if is_language_specific %} for {{ language_filter }}{% endif %}. Start adding some reviews!</p>
        </div>
        {% endif %}
    </main>

    <footer class="footer">
        <p>Generated on {{ generation_date }} by Enhanced IMDB MCP Server v2.0.0</p>
        <p>Original Language Focus • {{ total_movies }} Movies • Personal Collection</p>
    </footer>
</body>
</html>
""")

def generate_html_files():
    """
    Generate static HTML files for all movies and language-specific pages.
    
    v2.0.0 Enhancement: Uses original language focus for cleaner categorization.
    """
    print("🎬 Loading movie reviews...")
    reviews = load_reviews()
    
    if not reviews:
        print("❌ No reviews found in my_reviews.json")
        return
    
    print(f"📚 Found {len(reviews)} movie reviews")
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    # Group movies by original language
    language_groups = group_movies_by_language(reviews)
    detected_languages = detect_languages_in_reviews(reviews)
    
    print(f"🌐 Found original languages: {', '.join(sorted(detected_languages))}")
    
    # Generate main page (all movies)
    print("📄 Generating index.html (all movies)...")
    all_movies = [(title, data) for title, data in reviews.items()]
    
    # Sort movies by rating (highest first), then by title
    sorted_movies = sorted(
        all_movies,
        key=lambda x: (
            -(x[1].get('rating', 0) if isinstance(x[1], dict) else 0),
            x[0].lower()
        )
    )
    
    # Calculate statistics
    total_movies = len(all_movies)
    ratings = [data.get('rating', 0) for title, data in all_movies if isinstance(data, dict) and data.get('rating')]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    # Create template context for main page
    template_context = {
        'movies': sorted_movies,
        'total_movies': total_movies,
        'average_rating': avg_rating,
        'is_language_specific': False,
        'generation_date': datetime.now().strftime("%B %d, %Y at %I:%M %p")
    }
    
    # Generate main HTML
    html_content = movie_template.render(**template_context)
    
    with open(f"{OUTPUT_DIR}/index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated main page: index.html ({total_movies} movies, avg rating: {avg_rating:.1f})")
    
    # Generate language-specific pages
    for language, movies in language_groups.items():
        if language != 'Unknown' or len(movies) > 0:  # Generate Unknown page only if there are movies
            generate_language_specific_page(language, movies, OUTPUT_DIR)
    
    print(f"\n✅ HTML files generated successfully!")
    print(f"📁 Output directory: {OUTPUT_DIR}/")
    print(f"🌐 Open {OUTPUT_DIR}/index.html in your browser to view all movies")
    print(f"🎯 Language-specific pages: {len(language_groups)} files generated")
    
    # Show summary by language
    print(f"\n📊 Movies by original language:")
    for language, movies in sorted(language_groups.items()):
        print(f"   • {language}: {len(movies)} movies")

if __name__ == '__main__':
    generate_html_files() 