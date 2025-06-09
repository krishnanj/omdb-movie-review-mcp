#!/usr/bin/env python3
"""
Movie Review MCP Server - A Model Context Protocol server for movie search and personal review management.

This server provides tools to:
- Search for movies using the OMDb API (Open Movie Database) - READ ONLY
- Manage personal movie reviews with ratings and text - LOCAL STORAGE
- Export reviews in various formats for MANUAL posting to platforms
- Analyze rating patterns and statistics - LOCAL DATA

IMPORTANT LIMITATIONS:
- Uses OMDb API for movie data (not direct IMDb access)
- Cannot automatically post to IMDb, Letterboxd, or other platforms
- All posting to external platforms must be done manually
- OMDb provides movie metadata but is read-only

The server uses the FastMCP framework and communicates via JSON-RPC over stdio.

Architecture:
    Claude Desktop/Cursor → JSON-RPC → MCP Server → OMDb API (read-only)
                                            ↓
                                      Local JSON Reviews (read/write)

Author: Created for personal movie review management
Version: 1.0.0
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
   • IMDb Votes: {data.get('imdbVotes', 'N/A')}
   • Metascore: {data.get('Metascore', 'N/A')}/100

🔗 **IMDb Link:** https://www.imdb.com/title/{data.get('imdbID', '')}

💰 **Box Office:** {data.get('BoxOffice', 'Not available')}
🏆 **Awards:** {data.get('Awards', 'None listed')}

ℹ️ *This data is provided by OMDb API and may not reflect real-time IMDb information.*"""
        else:
            return f"❌ Movie '{title}' not found in OMDb database. Error: {data.get('Error', 'Unknown error')}"
            
    except requests.exceptions.RequestException as e:
        return f"❌ Network error searching OMDb for '{title}': {str(e)}"
    except Exception as e:
        return f"❌ Unexpected error searching OMDb for '{title}': {str(e)}"

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
    Automatically manages timestamps for tracking when reviews are added/modified.
    
    Args:
        title (str): Movie title to review
        rating (int): Numeric rating from 1-10 (1=terrible, 10=masterpiece)
        review (str): Detailed text review
        
    Returns:
        str: Confirmation message with review summary
        
    Example:
        write_review("Inception", 9, "Mind-bending masterpiece with incredible visuals")
        - Stores locally only, does NOT post to IMDb
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
        
        # Create review entry with full metadata (stored locally)
        reviews[normalized_title] = {
            "rating": rating,
            "review": review.strip(),
            "date_added": reviews.get(normalized_title, {}).get("date_added", current_time),
            "last_updated": current_time
        }
        
        # Save updated reviews to local file (NOT to IMDb)
        save_reviews(reviews)
        
        # Generate visual rating display
        stars = rating_to_stars(rating)
        action = "updated" if is_update else "added"
        
        return f"""✅ Review {action} successfully in local storage!

🎬 **{normalized_title}**
⭐ **Rating:** {rating}/10 {stars}
📝 **Review:** {review[:100]}{"..." if len(review) > 100 else ""}
📅 **{action.title()}:** {current_time}

💾 **Storage:** Local file only - use export tools to post to IMDb/Letterboxd manually"""
        
    except Exception as e:
        return f"❌ Error writing local review for '{title}': {str(e)}"

@mcp.tool()
def get_review(title: str) -> str:
    """
    Retrieve your personal review for a specific movie.
    
    Supports both new format (rating + text + timestamps) and legacy format (text only).
    
    Args:
        title (str): Movie title to look up
        
    Returns:
        str: Formatted review information or not found message
        
    Example:
        get_review("Inception") returns your rating, review text, and timestamps
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

⚠️ *Legacy review format - no rating or timestamp available*"""
        
        elif isinstance(review_data, dict):
            # New format - structured data
            rating = review_data.get("rating", "N/A")
            review_text = review_data.get("review", "No review text")
            date_added = review_data.get("date_added", "Unknown")
            last_updated = review_data.get("last_updated", "Unknown")
            
            stars = rating_to_stars(rating) if isinstance(rating, (int, float)) else "☆☆☆☆☆"
            
            return f"""📝 **Your Review for {normalized_title}:**

⭐ **Rating:** {rating}/10 {stars}
📖 **Review:** {review_text}

📅 **Added:** {date_added}
🔄 **Last Updated:** {last_updated}"""
        
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
            else:
                review_text = review_data
                rating_display = "Legacy format"
                date_info = "Unknown date"
            
            # Truncate long reviews for list display
            truncated_review = review_text[:80] + "..." if len(review_text) > 80 else review_text
            
            result += f"""
{i}. **{title}**
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