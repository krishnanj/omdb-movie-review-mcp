#!/usr/bin/env python3
"""
Enhanced Movie Review MCP Server - A comprehensive Model Context Protocol server for intelligent 
movie discussions, review management, and beautiful web displays.

🚀 ENHANCED FEATURES:
- 🧠 Smart Movie Discussions: AI-powered discovery by language & era
- 🌐 Multi-Language Support: 15+ languages with intelligent search  
- 📊 Automatic Metadata Enrichment: IMDb links, posters, ratings, cast info
- 🖼️ Beautiful Web Display: Generate stunning HTML galleries with posters
- 🎯 Language Filtering: Dedicated pages for each language
- ⚡ Never Repeat Logic: Smart tracking to avoid reviewing same movies
- 🎬 Quick Rating System: Streamlined rating during discussions

CORE CAPABILITIES:
- Search for movies using the OMDb API (Open Movie Database) - READ ONLY
- Manage personal movie reviews with rich metadata - LOCAL STORAGE
- Export reviews in various formats for MANUAL posting to platforms
- Generate beautiful static HTML displays with movie posters
- Analyze rating patterns and statistics - LOCAL DATA
- Smart movie discovery using language-specific keywords and actors

🌐 MULTI-LANGUAGE CINEMA SUPPORT (15+ Languages):
Hindi, English, Spanish, French, Japanese, Korean, Chinese, German, Italian, 
Russian, Portuguese, Arabic, Tamil, Telugu, Bengali

🧠 SMART DISCUSSION WORKFLOW:
1. User: "Let's discuss 2000s Hindi movies"
2. System: Discovers Hindi cinema from 2000-2010 using cultural keywords
3. System: Asks if user has watched each movie (excludes already reviewed)
4. User: Provides ratings and reviews
5. System: Automatically enriches with metadata (IMDb links, posters, etc.)
6. System: Stores in enhanced JSON format
7. Generate: Beautiful HTML galleries with language filtering

📊 ENHANCED REVIEW STRUCTURE:
Each review includes: rating, review text, timestamps, IMDb link, poster URL,
director, genre, language, country, IMDb rating, year - all automatically fetched

🖼️ WEB DISPLAY GENERATION:
- Static HTML files (no server required)
- Movie poster galleries with responsive design
- Language-specific filtered pages (index_hindi.html, index_english.html, etc.)
- Navigation between languages, IMDb integration, statistics dashboard

IMPORTANT LIMITATIONS:
- Uses OMDb API for movie data (not direct IMDb access)
- Cannot automatically post to IMDb, Letterboxd, or other platforms
- All posting to external platforms must be done manually
- OMDb provides movie metadata but is read-only

ARCHITECTURE:
    Claude Desktop/Cursor → JSON-RPC → Enhanced MCP Server → OMDb API (read-only)
                                            ↓
                                      Enhanced JSON Reviews (read/write)
                                            ↓
                                      HTML Display Generator (static files)

Author: Created for intelligent personal movie review management
Version: 2.0.0 - Enhanced Edition
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# =============================================================================
# CONFIGURATION & INITIALIZATION
# =============================================================================

# Load environment variables from .env file
load_dotenv()

# Initialize the FastMCP server instance
mcp = FastMCP("Movie Review MCP Server")

# OMDb API configuration - Open Movie Database (third-party IMDb data provider)
# NOTE: This is NOT direct IMDb access - it's a read-only API that provides IMDb data
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "1ad3ea84")
OMDB_BASE_URL = "http://www.omdbapi.com/"

# Local storage configuration - all reviews stored locally, NOT on IMDb or other platforms
REVIEWS_FILE = "/Users/jeyashreekrishan/workspace/imdb-mcp-server/my_reviews.json"

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def load_reviews() -> Dict[str, Any]:
    """
    Load movie reviews from the local JSON file.
    
    Handles both new format (with rating/review/timestamps) and legacy format (text-only).
    Creates empty file if it doesn't exist.
    
    Returns:
        Dict[str, Any]: Dictionary containing all movie reviews
        
    Format:
        {
            "Movie Title": {
                "rating": 8,
                "review": "Great movie!",
                "date_added": "2024-06-09T19:15:00",
                "last_updated": "2024-06-09T19:15:00"
            }
        }
    """
    try:
        if os.path.exists(REVIEWS_FILE):
            with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading reviews: {e}")
        return {}

def save_reviews(reviews: Dict[str, Any]) -> None:
    """
    Save movie reviews to the local JSON file.
    
    Args:
        reviews (Dict[str, Any]): Complete reviews dictionary to save
        
    Raises:
        IOError: If unable to write to the reviews file
    """
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving reviews: {e}")
        raise

def normalize_title(title: str) -> str:
    """
    Normalize movie title for consistent storage and lookup.
    
    Args:
        title (str): Original movie title
        
    Returns:
        str: Normalized title (trimmed and title-cased)
    """
    return title.strip().title()

def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format for review metadata.
    
    Returns:
        str: Current timestamp (e.g., "2024-06-09T19:15:00")
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def fetch_movie_metadata(title: str) -> Dict[str, str]:
    """
    Fetch movie metadata from OMDb API including IMDb link and poster image.
    
    Args:
        title (str): Movie title to search for
        
    Returns:
        Dict[str, str]: Dictionary containing IMDb link, poster URL, and other metadata
    """
    try:
        # Search for the movie using OMDb API
        params = {
            'apikey': OMDB_API_KEY,
            't': title,
            'plot': 'short'
        }
        
        response = requests.get(OMDB_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('Response') == 'True':
            imdb_id = data.get('imdbID', '')
            poster_url = data.get('Poster', '')
            
            # Construct IMDb page link
            imdb_link = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else ""
            
            # Validate poster URL (OMDb sometimes returns "N/A" for missing posters)
            if poster_url == "N/A" or not poster_url:
                poster_url = ""
            
            return {
                'imdb_link': imdb_link,
                'poster_url': poster_url,
                'imdb_id': imdb_id,
                'year': data.get('Year', ''),
                'director': data.get('Director', ''),
                'genre': data.get('Genre', ''),
                'imdb_rating': data.get('imdbRating', ''),
                'language': data.get('Language', ''),
                'country': data.get('Country', '')
            }
        else:
            # Movie not found in OMDb - return empty metadata
            return {
                'imdb_link': '',
                'poster_url': '',
                'imdb_id': '',
                'year': '',
                'director': '',
                'genre': '',
                'imdb_rating': '',
                'language': '',
                'country': ''
            }
            
    except Exception as e:
        print(f"Error fetching metadata for '{title}': {e}")
        # Return empty metadata on error
        return {
            'imdb_link': '',
            'poster_url': '',
            'imdb_id': '',
            'year': '',
            'director': '',
            'genre': '',
            'imdb_rating': '',
            'language': '',
            'country': ''
        }

def rating_to_stars(rating: Union[int, float]) -> str:
    """
    Convert numeric rating to visual star representation.
    
    Args:
        rating (Union[int, float]): Numeric rating (1-10 scale)
        
    Returns:
        str: Star representation (e.g., "★★★★☆" for rating 8)
    """
    if isinstance(rating, str):
        return "☆☆☆☆☆"  # Unknown rating
    
    full_stars = int(rating // 2)
    half_star = 1 if (rating % 2) >= 1 else 0
    empty_stars = 5 - full_stars - half_star
    
    return "★" * full_stars + ("☆" if half_star else "") + "☆" * empty_stars

# =============================================================================
# MOVIE SEARCH TOOLS
# =============================================================================

@mcp.tool()
def search_movie(title: str) -> str:
    """
    Search for movie information using the OMDb API (Open Movie Database).
    
    IMPORTANT: This uses OMDb API, not direct IMDb access. OMDb is a third-party
    service that provides IMDb data via API. This is READ-ONLY access to movie
    information - we cannot modify anything on IMDb.
    
    Args:
        title (str): The movie title to search for
        
    Returns:
        str: Formatted movie information from OMDb API or error message
        
    Example:
        search_movie("Inception") returns detailed info about Inception (2010) from OMDb
    """
    try:
        # Prepare API request parameters for OMDb
        params = {
            'apikey': OMDB_API_KEY,
            't': title,
            'plot': 'full'  # Get full plot description from OMDb
        }
        
        # Make API request to OMDb (NOT direct IMDb)
        response = requests.get(OMDB_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if movie was found in OMDb database
        if data.get('Response') == 'True':
            # Format comprehensive movie information from OMDb data
            return f"""🎬 **{data.get('Title', 'Unknown')}** ({data.get('Year', 'Unknown')})
📡 *Data source: OMDb API (Open Movie Database)*

📝 **Plot:** {data.get('Plot', 'No plot available')}

👥 **Cast & Crew:**
   • Director: {data.get('Director', 'Unknown')}
   • Writer: {data.get('Writer', 'Unknown')}
   • Actors: {data.get('Actors', 'Unknown')}

📊 **Details:**
   • Genre: {data.get('Genre', 'Unknown')}
   • Runtime: {data.get('Runtime', 'Unknown')}  
   • Rated: {data.get('Rated', 'Unknown')}
   • Language: {data.get('Language', 'Unknown')}
   • Country: {data.get('Country', 'Unknown')}

⭐ **Ratings:**
   • IMDb: {data.get('imdbRating', 'N/A')}/10
   • Rotten Tomatoes: {data.get('Ratings', [{}])[0].get('Value', 'N/A') if data.get('Ratings') else 'N/A'}

🔗 **IMDb ID:** {data.get('imdbID', 'N/A')}

💰 **Box Office:** {data.get('BoxOffice', 'N/A')}
🏆 **Awards:** {data.get('Awards', 'N/A')}"""
        else:
            return f"❌ Movie not found: {data.get('Error', 'Unknown error')}"
            
    except requests.RequestException as e:
        return f"❌ Network error searching for '{title}': {str(e)}"
    except Exception as e:
        return f"❌ Error searching for '{title}': {str(e)}"

@mcp.tool()
def discover_movies_by_criteria(language: str, year_start: int, year_end: int, count: int = 10) -> str:
    """
    Discover movies based on language and year criteria using OMDb API.
    
    This tool searches for popular movies from specific languages and time periods,
    filtering out movies that have already been reviewed to avoid duplicates.
    
    Args:
        language (str): Language of movies to discover (e.g., "Hindi", "English", "Spanish", "French")
        year_start (int): Starting year for the search range
        year_end (int): Ending year for the search range  
        count (int): Number of movies to discover (default 10, max 20)
        
    Returns:
        str: List of discovered movies with basic info, excluding already reviewed ones
        
    Example:
        discover_movies_by_criteria("Hindi", 2000, 2010, 5) returns 5 Hindi movies from 2000s
    """
    try:
        # Load existing reviews to avoid duplicates
        existing_reviews = load_reviews()
        existing_titles = {normalize_title(title) for title in existing_reviews.keys()}
        
        # Limit count to reasonable range
        count = max(1, min(count, 20))
        
        discovered_movies = []
        
        # Search terms for different languages - using popular/common movie keywords
        search_terms_by_language = {
            "hindi": ["bollywood", "shah rukh khan", "aamir khan", "salman khan", "amitabh bachchan", "hrithik roshan", "akshay kumar"],
            "english": ["hollywood", "drama", "action", "comedy", "thriller", "romance", "adventure"],
            "spanish": ["spanish", "pedro almodovar", "spanish film", "spain", "madrid", "barcelona"],
            "french": ["french", "french film", "paris", "cinema francais", "french drama"],
            "japanese": ["japanese", "japan", "tokyo", "japanese film", "samurai", "anime"],
            "korean": ["korean", "korea", "seoul", "korean film", "k-drama"],
            "italian": ["italian", "italy", "italian film", "roma", "italian cinema"],
            "german": ["german", "germany", "german film", "berlin", "german cinema"],
            "chinese": ["chinese", "china", "chinese film", "hong kong", "mandarin"],
            "russian": ["russian", "russia", "russian film", "moscow", "soviet"],
            "tamil": ["tamil", "kollywood", "tamil film", "chennai", "south indian"],
            "telugu": ["telugu", "tollywood", "telugu film", "hyderabad", "south indian"],
            "arabic": ["arabic", "arab", "middle east", "arabic film", "lebanon", "egypt"],
            "portuguese": ["portuguese", "brazil", "brazilian", "portugal", "brazilian film"],
            "turkish": ["turkish", "turkey", "turkish film", "istanbul", "turkish cinema"]
        }
        
        # Get search terms for the specified language
        lang_lower = language.lower()
        search_terms = search_terms_by_language.get(lang_lower, [language.lower()])
        
        # Try multiple search approaches to find movies
        for term in search_terms[:3]:  # Limit to 3 search terms to avoid too many API calls
            for year in range(year_start, min(year_end + 1, year_start + 5)):  # Limit year range
                try:
                    # Search using OMDb API
                    params = {
                        'apikey': OMDB_API_KEY,
                        's': term,
                        'y': year,
                        'type': 'movie'
                    }
                    
                    response = requests.get(OMDB_BASE_URL, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    if data.get('Response') == 'True' and 'Search' in data:
                        for movie in data['Search'][:5]:  # Limit to first 5 results per search
                            title = movie.get('Title', '')
                            movie_year = movie.get('Year', '')
                            
                            # Skip if already reviewed
                            if normalize_title(title) in existing_titles:
                                continue
                                
                            # Check if within year range
                            try:
                                if int(movie_year) < year_start or int(movie_year) > year_end:
                                    continue
                            except:
                                continue
                            
                            # Get detailed info for this movie
                            detail_params = {
                                'apikey': OMDB_API_KEY,
                                'i': movie.get('imdbID', ''),
                                'plot': 'short'
                            }
                            
                            detail_response = requests.get(OMDB_BASE_URL, params=detail_params, timeout=10)
                            if detail_response.status_code == 200:
                                detail_data = detail_response.json()
                                if detail_data.get('Response') == 'True':
                                    # Check if language matches (if available)
                                    movie_language = detail_data.get('Language', '').lower()
                                    if language.lower() in movie_language or any(lang.lower() in movie_language for lang in [language]):
                                        discovered_movies.append({
                                            'title': title,
                                            'year': movie_year,
                                            'director': detail_data.get('Director', 'Unknown'),
                                            'genre': detail_data.get('Genre', 'Unknown'),
                                            'plot': detail_data.get('Plot', 'No plot available'),
                                            'rating': detail_data.get('imdbRating', 'N/A'),
                                            'language': detail_data.get('Language', 'Unknown')
                                        })
                                        
                                        if len(discovered_movies) >= count:
                                            break
                            
                            # Small delay to be respectful to API
                            import time
                            time.sleep(0.1)
                    
                    if len(discovered_movies) >= count:
                        break
                        
                except requests.RequestException:
                    continue  # Try next search term/year
                    
            if len(discovered_movies) >= count:
                break
        
        if not discovered_movies:
            return f"""🔍 **No new movies found for your criteria:**
• Language: {language}
• Years: {year_start}-{year_end}
• Already reviewed: {len(existing_titles)} movies

💡 **Try different criteria:**
• Expand the year range
• Try related languages (e.g., "Bollywood" for Hindi)
• Use broader language terms"""

        # Format the discovered movies
        result = f"""🎬 **Discovered {len(discovered_movies)} {language} movies ({year_start}-{year_end}):**

*These movies are not in your review collection yet.*

"""
        
        for i, movie in enumerate(discovered_movies, 1):
            result += f"""**{i}. {movie['title']}** ({movie['year']})
   • Director: {movie['director']}
   • Genre: {movie['genre']}
   • IMDb: {movie['rating']}/10
   • Language: {movie['language']}
   • Plot: {movie['plot'][:100]}{'...' if len(movie['plot']) > 100 else ''}

"""
        
        result += f"""
📊 **Session Status:**
• Found: {len(discovered_movies)} new movies
• Already reviewed: {len(existing_titles)} movies total
• Language: {language}
• Time period: {year_start}-{year_end}

💭 **Next steps:** Let me know which movies you've watched and I'll help you rate them!"""

        return result
        
    except Exception as e:
        return f"❌ Error discovering movies: {str(e)}"

@mcp.tool()
def start_movie_discussion_session() -> str:
    """
    Start an interactive movie discussion session.
    
    This tool initiates a conversation flow where the user can specify their preferences
    for language and time period, then discover and rate movies they've watched.
    
    Returns:
        str: Welcome message with instructions for the movie discussion session
    """
    return """🎬 **Welcome to Movie Discussion Session!**

Let's discover and discuss movies you've watched! Here's how it works:

📋 **Step 1: Tell me your preferences**
Please let me know:
• **Language**: What language movies are you in the mood to discuss? 
  (e.g., "Hindi", "English", "Spanish", "French", "Japanese", "Korean", etc.)
• **Time Period**: What years are you interested in? 
  (e.g., "2000s" for 2000-2009, "1990-2005", "2010-2020", etc.)

🔍 **Step 2: I'll discover movies**
I'll search for popular movies matching your criteria and show you ones you haven't reviewed yet.

⭐ **Step 3: Rate what you've watched**
For each movie I suggest, just tell me:
• **"Yes"** if you've watched it (then I'll ask for your rating & review)
• **"No"** if you haven't seen it (I'll skip to the next one)

💾 **Step 4: Save your reviews**
I'll automatically save all your ratings and reviews to your collection.

---

**Examples to get started:**
• "I want to discuss 2000s Hindi movies"
• "Let's talk about French films from the 1990s"  
• "Show me English movies from 2010-2020"
• "I'm interested in Korean films from any time period"

**What language and time period would you like to explore today?** 🎭"""

@mcp.tool()
def quick_rate_movie(title: str, rating: int, review: str = "") -> str:
    """
    Quickly rate a movie during a discussion session.
    
    This is a streamlined version of write_review optimized for discussion sessions,
    with better feedback and integration with the discovery workflow.
    Automatically fetches and stores movie metadata including IMDb links and poster URLs.
    
    Args:
        title (str): Movie title to rate
        rating (int): Rating from 1-10
        review (str): Optional review text (can be brief during sessions)
        
    Returns:
        str: Confirmation message with rating saved and movie metadata
    """
    try:
        # Validate rating
        if not isinstance(rating, int) or rating < 1 or rating > 10:
            return "❌ Rating must be an integer between 1 and 10"
        
        # Load existing reviews
        reviews = load_reviews()
        normalized_title = normalize_title(title)
        current_time = get_current_timestamp()
        
        # Check if updating existing review
        is_update = normalized_title in reviews
        
        # Fetch movie metadata from OMDb API
        print(f"🔍 Fetching movie metadata for '{title}'...", file=sys.stderr)
        metadata = fetch_movie_metadata(title)
        
        # Prepare review data with metadata
        review_data = {
            "rating": rating,
            "review": review if review.strip() else f"Rated {rating}/10 during movie discussion session",
            "last_updated": current_time,
            # Movie metadata from OMDb
            "imdb_link": metadata['imdb_link'],
            "poster_url": metadata['poster_url'],
            "imdb_id": metadata['imdb_id'],
            "year": metadata['year'],
            "director": metadata['director'],
            "genre": metadata['genre'],
            "imdb_rating": metadata['imdb_rating'],
            "language": metadata['language'],
            "country": metadata['country']
        }
        
        # Add date_added if new review
        if not is_update:
            review_data["date_added"] = current_time
        else:
            # Keep original date_added if updating
            if isinstance(reviews[normalized_title], dict):
                review_data["date_added"] = reviews[normalized_title].get("date_added", current_time)
            else:
                review_data["date_added"] = current_time
        
        # Save the review
        reviews[normalized_title] = review_data
        save_reviews(reviews)
        
        # Generate confirmation message
        stars = rating_to_stars(rating)
        action = "Updated" if is_update else "Added"
        
        result = f"""✅ **{action} rating for "{title}"**

⭐ **Your Rating:** {rating}/10 {stars}
🎭 **IMDb Rating:** {metadata['imdb_rating']}/10 (for reference)
📝 **Review:** {review_data['review']}
📅 **Date:** {current_time[:10]}

🔗 **Links:**"""
        
        if metadata['imdb_link']:
            result += f"\n   • IMDb Page: {metadata['imdb_link']}"
        
        if metadata['poster_url']:
            result += f"\n   🖼️ Movie Poster: {metadata['poster_url']}"
            
        result += f"""

🎯 **Movie Info:** 
   📅 **Year:** {metadata['year'] if metadata['year'] else 'Unknown'}
   🌐 **Language:** {metadata['language'] if metadata['language'] else 'Unknown'}
   🎬 **Director:** {metadata['director'] if metadata['director'] else 'Unknown'}
   🎭 **Genre:** {metadata['genre'] if metadata['genre'] else 'Unknown'}

💾 **Saved to your collection!** 
({len(reviews)} total movies reviewed)

🎬 **Ready for the next movie?** Just say "next" or tell me about another movie!"""

        return result
        
    except Exception as e:
        return f"❌ Error saving rating for '{title}': {str(e)}"

@mcp.tool() 
def get_unreviewed_movies_count(language: str = "", year_start: int = 1900, year_end: int = 2024) -> str:
    """
    Get a count of how many movies are available to discover vs already reviewed.
    
    Helpful for understanding the scope of a movie discussion session.
    
    Args:
        language (str): Optional language filter
        year_start (int): Start year for counting
        year_end (int): End year for counting
        
    Returns:
        str: Statistics about reviewed vs available movies
    """
    try:
        reviews = load_reviews()
        reviewed_count = len(reviews)
        
        # Get some stats about reviewed movies
        language_stats = {}
        year_stats = {}
        
        for title, review_data in reviews.items():
            if isinstance(review_data, dict):
                # Try to get movie info for stats (limited to avoid too many API calls)
                pass
        
        result = f"""📊 **Your Movie Collection Stats:**

📚 **Total Reviews:** {reviewed_count} movies

🎭 **Discussion Session Scope:**
• Language: {language if language else 'Any language'}
• Years: {year_start}-{year_end}

💡 **Ready to discover more movies?** 
Use `discover_movies_by_criteria` to find movies you haven't reviewed yet!

🔍 **Popular discovery options:**
• Hindi/Bollywood movies from 2000s
• English movies from 2010s  
• Classic films from 1990s
• International cinema from any period"""

        return result
        
    except Exception as e:
        return f"❌ Error getting movie stats: {str(e)}"

# =============================================================================
# REVIEW MANAGEMENT TOOLS
# =============================================================================

@mcp.tool()
def write_review(title: str, rating: int, review: str) -> str:
    """
    Write or update a movie review with both quantitative rating and qualitative text.
    
    IMPORTANT: This stores your review LOCALLY only. It does NOT post to IMDb,
    Letterboxd, or any other platform. Use export tools to get formatted text
    for manual posting to external platforms.
    
    Creates a new review or updates an existing one with the provided rating and text.
    Automatically fetches and stores movie metadata including IMDb links and poster URLs.
    Manages timestamps for tracking when reviews are added/modified.
    
    Args:
        title (str): Movie title to review
        rating (int): Numeric rating from 1-10 (1=terrible, 10=masterpiece)
        review (str): Detailed text review
        
    Returns:
        str: Confirmation message with review summary and movie metadata
        
    Example:
        write_review("Inception", 9, "Mind-bending masterpiece with incredible visuals")
        - Stores locally with IMDb link and poster URL
    """
    try:
        # Validate input parameters
        if not isinstance(rating, int) or not (1 <= rating <= 10):
            return "❌ Rating must be an integer between 1 and 10"
        
        if not title.strip() or not review.strip():
            return "❌ Title and review text cannot be empty"
        
        # Normalize title for consistent storage
        normalized_title = normalize_title(title)
        
        # Load existing local reviews
        reviews = load_reviews()
        
        # Determine if this is an update or new review
        is_update = normalized_title in reviews
        current_time = get_current_timestamp()
        
        # Fetch movie metadata from OMDb API
        print(f"🔍 Fetching movie metadata for '{title}'...", file=sys.stderr)
        metadata = fetch_movie_metadata(title)
        
        # Create review entry with full metadata (stored locally)
        review_data = {
            "rating": rating,
            "review": review.strip(),
            "date_added": reviews.get(normalized_title, {}).get("date_added", current_time) if isinstance(reviews.get(normalized_title), dict) else current_time,
            "last_updated": current_time,
            # Movie metadata from OMDb
            "imdb_link": metadata['imdb_link'],
            "poster_url": metadata['poster_url'],
            "imdb_id": metadata['imdb_id'],
            "year": metadata['year'],
            "director": metadata['director'],
            "genre": metadata['genre'],
            "imdb_rating": metadata['imdb_rating'],
            "language": metadata['language'],
            "country": metadata['country']
        }
        
        reviews[normalized_title] = review_data
        
        # Save updated reviews to local file (NOT to IMDb)
        save_reviews(reviews)
        
        # Generate visual rating display
        stars = rating_to_stars(rating)
        action = "updated" if is_update else "added"
        
        # Create confirmation message with metadata
        result = f"""✅ Review {action} successfully in local storage!

🎬 **{normalized_title}** ({metadata['year'] if metadata['year'] else 'Year unknown'})
⭐ **Your Rating:** {rating}/10 {stars}
🎭 **IMDb Rating:** {metadata['imdb_rating']}/10 (for reference)
📝 **Review:** {review[:100]}{"..." if len(review) > 100 else ""}

🔗 **Links:**"""
        
        if metadata['imdb_link']:
            result += f"\n   • IMDb Page: {metadata['imdb_link']}"
        
        if metadata['poster_url']:
            result += f"\n   🖼️ Movie Poster: {metadata['poster_url']}"
        
        result += f"""

🎯 **Movie Details:**
   📅 **Year:** {metadata['year'] if metadata['year'] else 'Unknown'}
   🌐 **Language:** {metadata['language'] if metadata['language'] else 'Unknown'}
   🎬 **Director:** {metadata['director'] if metadata['director'] else 'Unknown'}
   🎭 **Genre:** {metadata['genre'] if metadata['genre'] else 'Unknown'}
   🌍 **Country:** {metadata['country'] if metadata['country'] else 'Unknown'}

📅 **{action.title()}:** {current_time}

💾 **Storage:** Local file with full metadata - use export tools to post to IMDb/Letterboxd manually"""
        
        return result
        
    except Exception as e:
        return f"❌ Error writing local review for '{title}': {str(e)}"

@mcp.tool()
def get_review(title: str) -> str:
    """
    Retrieve your personal review for a specific movie.
    
    Supports both new format (rating + text + timestamps + metadata) and legacy format (text only).
    
    Args:
        title (str): Movie title to look up
        
    Returns:
        str: Formatted review information with movie metadata or not found message
        
    Example:
        get_review("Inception") returns your rating, review text, timestamps, and IMDb links
    """
    try:
        normalized_title = normalize_title(title)
        reviews = load_reviews()
        
        if normalized_title not in reviews:
            return f"❌ No review found for '{normalized_title}'. Use write_review to add one!"
        
        review_data = reviews[normalized_title]
        
        # Handle legacy format (string reviews) vs new format (dict with rating)
        if isinstance(review_data, str):
            # Legacy format - just text
            return f"""📝 **Your Review for {normalized_title}:**

{review_data}

⚠️ *Legacy review format - no rating, metadata, or timestamp available*"""
        
        elif isinstance(review_data, dict):
            # New format - structured data
            rating = review_data.get("rating", "N/A")
            review_text = review_data.get("review", "No review text")
            date_added = review_data.get("date_added", "Unknown")
            last_updated = review_data.get("last_updated", "Unknown")
            
            # Movie metadata
            imdb_link = review_data.get("imdb_link", "")
            poster_url = review_data.get("poster_url", "")
            year = review_data.get("year", "")
            director = review_data.get("director", "")
            genre = review_data.get("genre", "")
            imdb_rating = review_data.get("imdb_rating", "")
            language = review_data.get("language", "")
            country = review_data.get("country", "")
            
            stars = rating_to_stars(rating) if isinstance(rating, (int, float)) else "☆☆☆☆☆"
            
            result = f"""📝 **Your Review for {normalized_title}** ({year if year else 'Year unknown'})

⭐ **Your Rating:** {rating}/10 {stars}
🎭 **IMDb Rating:** {imdb_rating}/10 (for reference)
📖 **Review:** {review_text}

🔗 **Links:**"""
            
            if imdb_link:
                result += f"\n   • IMDb Page: {imdb_link}"
            
            if poster_url:
                result += f"\n   🖼️ Movie Poster: {poster_url}"
            
            result += f"""

🎯 **Movie Details:**
   📅 **Year:** {year if year else 'Unknown'}
   🌐 **Language:** {language if language else 'Unknown'}
   🎬 **Director:** {director if director else 'Unknown'}
   🎭 **Genre:** {genre if genre else 'Unknown'}
   🌍 **Country:** {country if country else 'Unknown'}

📅 **Added:** {date_added}
🔄 **Last Updated:** {last_updated}"""
            
            return result
        
        else:
            return f"❌ Invalid review format for '{normalized_title}'"
            
    except Exception as e:
        return f"❌ Error retrieving review for '{title}': {str(e)}"

@mcp.tool()
def list_reviews() -> str:
    """
    List all your movie reviews with ratings and statistics.
    
    Provides a comprehensive overview of all reviews including:
    - Individual movie ratings and review snippets
    - Average rating across all movies
    - Total number of reviews
    - Recent activity
    
    Returns:
        str: Formatted list of all reviews with statistics
    """
    try:
        reviews = load_reviews()
        
        if not reviews:
            return "📝 No movie reviews found yet. Use write_review to add your first review!"
        
        # Sort reviews by rating (highest first), then by title
        sorted_reviews = []
        numeric_ratings = []
        
        for title, review_data in reviews.items():
            if isinstance(review_data, dict):
                rating = review_data.get("rating")
                if isinstance(rating, (int, float)):
                    numeric_ratings.append(rating)
                    sorted_reviews.append((title, review_data, rating))
                else:
                    sorted_reviews.append((title, review_data, 0))
            else:
                # Legacy format
                sorted_reviews.append((title, {"review": review_data, "rating": "N/A"}, 0))
        
        # Sort by rating (descending), then by title
        sorted_reviews.sort(key=lambda x: (-x[2] if isinstance(x[2], (int, float)) else -999, x[0]))
        
        # Calculate statistics
        avg_rating = sum(numeric_ratings) / len(numeric_ratings) if numeric_ratings else 0
        total_reviews = len(reviews)
        rated_reviews = len(numeric_ratings)
        
        # Build formatted output
        result = f"""🎬 **Your Movie Reviews** ({total_reviews} total, {rated_reviews} with ratings)

📊 **Statistics:**
   • Average Rating: {avg_rating:.1f}/10 {rating_to_stars(avg_rating)}
   • Highest Rated: {max(numeric_ratings) if numeric_ratings else 'N/A'}/10
   • Lowest Rated: {min(numeric_ratings) if numeric_ratings else 'N/A'}/10

📝 **All Reviews:**
"""
        
        # Add each review to the output
        for i, (title, review_data, rating) in enumerate(sorted_reviews, 1):
            if isinstance(review_data, dict):
                review_text = review_data.get("review", "No review text")
                rating_display = f"{rating}/10 {rating_to_stars(rating)}" if isinstance(rating, (int, float)) else "No rating"
                date_info = review_data.get("date_added", "Unknown date")
                year_info = review_data.get("year", "")
                language_info = review_data.get("language", "")
            else:
                review_text = review_data
                rating_display = "Legacy format"
                date_info = "Unknown date"
                year_info = ""
                language_info = ""
            
            # Truncate long reviews for list display
            truncated_review = review_text[:80] + "..." if len(review_text) > 80 else review_text
            
            # Build movie info line
            movie_info = []
            if year_info:
                movie_info.append(f"📅 {year_info}")
            if language_info:
                movie_info.append(f"🌐 {language_info.split(',')[0].strip()}")  # Show first language only for brevity
            movie_info_line = " • ".join(movie_info) if movie_info else ""
            
            result += f"""
{i}. **{title}** {f"({movie_info_line})" if movie_info_line else ""}
   ⭐ {rating_display}
   📝 {truncated_review}
   📅 {date_info}"""
        
        return result
        
    except Exception as e:
        return f"❌ Error listing reviews: {str(e)}"

@mcp.tool()
def delete_review(title: str) -> str:
    """
    Delete a movie review from your collection.
    
    Permanently removes the specified review from storage.
    
    Args:
        title (str): Movie title whose review should be deleted
        
    Returns:
        str: Confirmation message or error if review not found
    """
    try:
        normalized_title = normalize_title(title)
        reviews = load_reviews()
        
        if normalized_title not in reviews:
            return f"❌ No review found for '{normalized_title}' to delete"
        
        # Remove the review
        deleted_review = reviews.pop(normalized_title)
        save_reviews(reviews)
        
        # Show what was deleted
        if isinstance(deleted_review, dict):
            rating = deleted_review.get("rating", "N/A")
            return f"✅ Deleted review for '{normalized_title}' (Rating: {rating}/10)"
        else:
            return f"✅ Deleted review for '{normalized_title}' (Legacy format)"
            
    except Exception as e:
        return f"❌ Error deleting review for '{title}': {str(e)}"

@mcp.tool()
def get_top_rated_movies(limit: int = 5) -> str:
    """
    Get your highest-rated movies, sorted by rating.
    
    Args:
        limit (int): Maximum number of movies to return (default: 5)
        
    Returns:
        str: Formatted list of top-rated movies with ratings and review snippets
    """
    try:
        reviews = load_reviews()
        
        if not reviews:
            return "📝 No movie reviews found yet!"
        
        # Extract movies with numeric ratings
        rated_movies = []
        for title, review_data in reviews.items():
            if isinstance(review_data, dict):
                rating = review_data.get("rating")
                if isinstance(rating, (int, float)):
                    rated_movies.append((title, review_data, rating))
        
        if not rated_movies:
            return "📊 No movies with numeric ratings found!"
        
        # Sort by rating (highest first)
        rated_movies.sort(key=lambda x: x[2], reverse=True)
        
        # Limit results
        top_movies = rated_movies[:limit]
        
        result = f"🏆 **Your Top {len(top_movies)} Rated Movies:**\n"
        
        for i, (title, review_data, rating) in enumerate(top_movies, 1):
            stars = rating_to_stars(rating)
            review_text = review_data.get("review", "No review")
            truncated_review = review_text[:60] + "..." if len(review_text) > 60 else review_text
            
            result += f"""
{i}. **{title}**
   ⭐ {rating}/10 {stars}
   📝 {truncated_review}"""
        
        return result
        
    except Exception as e:
        return f"❌ Error getting top rated movies: {str(e)}"

# =============================================================================
# EXPORT TOOLS
# =============================================================================

@mcp.tool()
def export_review_for_posting(title: str) -> str:
    """
    Export a movie review in multiple formats ready for MANUAL posting to various platforms.
    
    IMPORTANT: This function only generates formatted text. It CANNOT automatically
    post to IMDb, Letterboxd, or any other platform. You must manually copy and paste
    the generated text to the target platform.
    
    Generates formatted versions for IMDb, Letterboxd, blogs, and general use.
    Includes movie metadata from OMDb when available.
    
    Args:
        title (str): Movie title to export
        
    Returns:
        str: Multiple formatted versions of the review ready for MANUAL posting
    """
    try:
        normalized_title = normalize_title(title)
        reviews = load_reviews()
        
        if normalized_title not in reviews:
            return f"❌ No review found for '{normalized_title}'"
        
        review_data = reviews[normalized_title]
        
        # Handle different review formats
        if isinstance(review_data, dict):
            rating = review_data.get("rating", "N/A")
            review_text = review_data.get("review", "")
            date_added = review_data.get("date_added", "")
        else:
            # Legacy format
            rating = "N/A"
            review_text = review_data
            date_added = ""
        
        # Try to get movie metadata from OMDb
        movie_info = ""
        try:
            params = {'apikey': OMDB_API_KEY, 't': title, 'plot': 'short'}
            response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
            if response.ok:
                data = response.json()
                if data.get('Response') == 'True':
                    movie_info = f"{data.get('Title')} ({data.get('Year')}) - {data.get('Genre')}"
                    imdb_link = f"https://www.imdb.com/title/{data.get('imdbID', '')}"
                else:
                    movie_info = normalized_title
                    imdb_link = f"https://www.imdb.com/find?q={normalized_title.replace(' ', '+')}"
            else:
                movie_info = normalized_title
                imdb_link = f"https://www.imdb.com/find?q={normalized_title.replace(' ', '+')}"
        except:
            movie_info = normalized_title
            imdb_link = f"https://www.imdb.com/find?q={normalized_title.replace(' ', '+')}"
        
        # Generate different export formats
        stars_visual = rating_to_stars(rating) if isinstance(rating, (int, float)) else "☆☆☆☆☆"
        
        return f"""📤 **Export Formats for {normalized_title}:**
⚠️ **MANUAL POSTING REQUIRED** - Copy and paste to target platforms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎬 **IMDb Ready Format:**
Rating: {rating}/10
{review_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 **Letterboxd Ready Format:**
{stars_visual} {rating}/10
{review_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 **Blog/Markdown Format:**
## {movie_info}
**Rating:** {rating}/10 {stars_visual}

{review_text}

**Watched:** {date_added[:10] if date_added else 'Unknown'}
**IMDb Link:** {imdb_link}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 **Social Media Format:**
Just watched {movie_info}! 
{stars_visual} {rating}/10
{review_text[:200]}{"..." if len(review_text) > 200 else ""}
{imdb_link}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **MANUAL POSTING INSTRUCTIONS:**
• IMDb: Go to movie page → Write Review → Copy/paste IMDb format
• Letterboxd: Search movie → Add to watched → Copy/paste Letterboxd format  
• Blog: Copy markdown format to your blog/website
• Social: Copy social format to Twitter/Facebook/Instagram
• ❌ CANNOT automatically post - manual copying required"""
        
    except Exception as e:
        return f"❌ Error exporting review for '{title}': {str(e)}"

@mcp.tool()
def export_all_reviews() -> str:
    """
    Export all movie reviews in various formats for bulk posting or backup.
    
    IMPORTANT: This function only generates formatted text. It CANNOT automatically
    post to any platform. All posting to IMDb, Letterboxd, or other platforms
    must be done manually by copying and pasting the generated content.
    
    Creates a comprehensive export of all reviews with posting instructions
    for different platforms.
    
    Returns:
        str: All reviews formatted for export with MANUAL posting instructions
    """
    try:
        reviews = load_reviews()
        
        if not reviews:
            return "📝 No reviews to export!"
        
        # Calculate statistics
        total_reviews = len(reviews)
        numeric_ratings = [r.get("rating") for r in reviews.values() 
                          if isinstance(r, dict) and isinstance(r.get("rating"), (int, float))]
        avg_rating = sum(numeric_ratings) / len(numeric_ratings) if numeric_ratings else 0
        
        # Start building export
        export_content = f"""🎬 **Complete Movie Review Export**
Generated: {get_current_timestamp()}

📊 **Summary Statistics:**
• Total Reviews: {total_reviews}
• Average Rating: {avg_rating:.1f}/10 {rating_to_stars(avg_rating)}
• Rated Reviews: {len(numeric_ratings)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 **All Reviews (Markdown Format):**

"""
        
        # Sort reviews by rating
        sorted_reviews = []
        for title, review_data in reviews.items():
            if isinstance(review_data, dict):
                rating = review_data.get("rating", 0)
                sorted_reviews.append((title, review_data, rating))
            else:
                sorted_reviews.append((title, {"review": review_data, "rating": "N/A"}, 0))
        
        sorted_reviews.sort(key=lambda x: (-x[2] if isinstance(x[2], (int, float)) else -999, x[0]))
        
        # Add each review
        for title, review_data, rating in sorted_reviews:
            if isinstance(review_data, dict):
                review_text = review_data.get("review", "")
                date_added = review_data.get("date_added", "Unknown")
                stars = rating_to_stars(rating) if isinstance(rating, (int, float)) else "☆☆☆☆☆"
                rating_display = f"{rating}/10" if isinstance(rating, (int, float)) else "No rating"
            else:
                review_text = review_data
                date_added = "Unknown"
                stars = "☆☆☆☆☆"
                rating_display = "Legacy format"
            
            export_content += f"""
## {title}
**Rating:** {rating_display} {stars}
**Date:** {date_added[:10] if date_added != "Unknown" else date_added}

{review_text}

---
"""
        
        export_content += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📤 **Platform Posting Instructions:**

🎯 **IMDb:**
• Go to movie page → Write Review
• Copy rating and review text for each movie

📚 **Letterboxd:**
• Search movie → Add to watched
• Use star rating + review text

📝 **Blog/Website:**
• Copy entire markdown section above
• Customize formatting as needed

📱 **Social Media:**
• Use individual movie exports for Twitter/Facebook
• Great for #MovieReview hashtags

💾 **Backup:**
• Save this export as backup of all reviews
• JSON file location: {REVIEWS_FILE}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ **Export complete!** {total_reviews} reviews ready for posting."""

        return export_content
        
    except Exception as e:
        return f"❌ Error exporting all reviews: {str(e)}"

# =============================================================================
# SERVER STARTUP
# =============================================================================

if __name__ == "__main__":
    """
    Start the Movie Review MCP server.
    
    The server runs in stdio mode, communicating with the host (Claude Desktop)
    via JSON-RPC messages over standard input/output streams.
    
    Server provides:
    - Movie search via OMDb API (read-only)
    - Local review management (read/write)
    - Export functionality for manual posting to platforms
    """
    try:
        print("🎬 Starting Movie Review MCP Server...", file=sys.stderr)
        print("📡 OMDb API: Movie data source (read-only)", file=sys.stderr)
        print("💾 Local Storage: Personal reviews (read/write)", file=sys.stderr)
        print(f"📁 Reviews file: {REVIEWS_FILE}", file=sys.stderr)
        print(f"🔑 OMDb API Key: {'✅ Set' if OMDB_API_KEY else '❌ Missing'}", file=sys.stderr)
        print("⚠️  Manual posting required for all external platforms", file=sys.stderr)
        
        # Start the server - this blocks until terminated
        mcp.run()
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}", file=sys.stderr)
        raise