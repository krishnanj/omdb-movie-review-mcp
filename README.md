# 🎬 Movie Review MCP Server - Painless Way To Keep Track of Your Movie Reviews

A comprehensive Model Context Protocol (MCP) server for intelligent movie discussions, review management, and beautiful web displays. Features smart movie discovery, automatic metadata enrichment, and stunning HTML visualizations.

**🚀 Latest Features:**
- **🧠 Smart Movie Discussions** - AI-powered movie discovery by language & era
- **🖼️ Beautiful Web Display** - Generate stunning HTML galleries with posters
- **🌐 Multi-Language Support** - 15+ languages with intelligent search
- **📊 Automatic Metadata** - IMDb links, posters, ratings, and cast info
- **🎯 Language Filtering** - Dedicated pages for each language
- **⚡ Never Repeat** - Smart tracking to avoid reviewing same movies

## 📋 Table of Contents

- [🎯 Overview](#overview)
- [✨ Features](#features)
- [🏗️ Architecture](#architecture)
- [📁 Project Structure](#project-structure)
- [🚀 Installation](#installation)
- [🛠️ Available Tools](#available-tools)
- [🧠 Smart Discussion System](#smart-discussion-system)
- [🌐 Multi-Language Support](#multi-language-support)
- [🖼️ Web Display Generation](#web-display-generation)
- [📊 Enhanced Review System](#enhanced-review-system)
- [📤 Export Functionality](#export-functionality)
- [🔧 Troubleshooting](#troubleshooting)
- [🤝 Contributing](#contributing)

## 🎯 Overview

This MCP server transforms movie review management from basic storage to an **intelligent discussion platform**. It combines:

- **OMDb API** for comprehensive movie data
- **Smart Discovery** using language-specific keywords and actors
- **Automatic Metadata Enrichment** with IMDb links and poster images
- **Beautiful Static HTML Generation** for web display
- **Multi-Language Cinema Support** with cultural context
- **Never-Repeat Logic** to track your viewing history

**⚠️ Important:** Uses OMDb API (not direct IMDb access). All posting to external platforms requires manual copy-paste.

## ✨ Features

### 🧠 Intelligent Movie Discovery
- **Smart Discussion Sessions** - "Let's discuss 2000s Hindi movies"
- **Language-Aware Search** - Uses actor names and cultural keywords
- **Era-Based Discovery** - Find movies by decade and year range
- **Never Repeat Logic** - Automatically excludes already-reviewed movies
- **Statistical Tracking** - Count unreviewed movies by criteria

### 🌐 Multi-Language Cinema Support
**15+ Languages Supported:**
- **Hindi** (Bollywood classics, contemporary hits)
- **English** (Hollywood, international English cinema)  
- **Spanish** (Spain & Latin America)
- **French** (French cinema classics)
- **Japanese** (Anime, live-action)
- **Korean** (K-dramas, Korean cinema)
- **Chinese** (Mandarin cinema)
- **German** (German films)
- **Italian** (Italian cinema)
- **Russian** (Russian films)
- **Portuguese** (Brazilian & Portuguese cinema)
- **Arabic** (Middle Eastern cinema)
- **Tamil** (South Indian cinema)
- **Telugu** (South Indian cinema)
- **Bengali** (Bengali cinema)

### 🖼️ Beautiful Web Display System
- **Static HTML Generation** - No server required, works offline
- **Movie Poster Galleries** - Visual display with IMDb poster images
- **Language Filtering** - Dedicated pages for each language
- **Responsive Design** - Beautiful on desktop and mobile
- **IMDb Integration** - Direct links to movie pages
- **Statistics Dashboard** - Total movies, average ratings, languages

### 📊 Automatic Metadata Enrichment
Every review automatically includes:
- **📅 Year** - Release year prominently displayed
- **🌐 Language** - Language(s) prominently displayed
- **🎬 Director** - Director information
- **🎭 Genre** - Movie genres
- **⭐ IMDb Rating** - Official IMDb rating for reference
- **🖼️ Poster Image** - High-quality movie poster
- **🔗 IMDb Link** - Direct link to IMDb page
- **🌍 Country** - Country of origin

### 🎯 Enhanced Review Management
- **Quick Rating** - Streamlined rating during discussions
- **Rich Text Reviews** - Detailed qualitative feedback
- **Star Visualization** - Beautiful ★★★★★ display
- **Statistics & Analytics** - Top movies, averages, trends
- **Batch Export** - Multiple format support for sharing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Desktop / Cursor                  │
│                      (MCP Host)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │ JSON-RPC over stdio
                      │
┌─────────────────────▼───────────────────────────────────────┐
│         Enhanced Movie Review MCP Server (main.py)         │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                FastMCP Framework                    │  │
│  │                                                     │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │Smart Movie  │  │ Enhanced    │  │ Web Display │ │  │
│  │  │Discovery    │  │ Reviews     │  │ Generator   │ │  │
│  │  │• Language   │  │• Metadata   │  │• Static HTML│ │  │
│  │  │• Era Search │  │• Posters    │  │• Language   │ │  │
│  │  │• Never      │  │• IMDb Links │  │  Filtering  │ │  │
│  │  │  Repeat     │  │• Analytics  │  │• Responsive │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────┬──────────────┬────────────────────────┘
                      │              │
        ┌─────────────▼─┐          ┌─▼──────────────┐
        │   OMDb API    │          │Enhanced JSON   │
        │• Movie Data   │          │• Rich Metadata │
        │• IMDb IDs     │          │• Poster URLs   │
        │• Poster URLs  │          │• IMDb Links    │
        │• Multi-Lang   │          │• Language Tags │
        └───────────────┘          └─────────────────┘
                                            │
                              ┌─────────────▼─────────────┐
                              │    Web Display System     │
                              │• index.html (all movies)  │
                              │• index_hindi.html         │
                              │• index_english.html       │
                              │• Beautiful galleries      │
                              └───────────────────────────┘
```

**Enhanced Data Flow:**
- **Smart Discovery**: Language/Era → OMDb Search → Filtered Results → User Discussion
- **Metadata Enrichment**: Movie Title → OMDb API → Rich Data → Enhanced JSON Storage
- **Web Generation**: Enhanced JSON → Jinja2 Templates → Static HTML → Beautiful Display
- **Language Filtering**: Multi-lang JSON → Separated HTML Pages → Navigation Links

## 📁 Project Structure

```
imdb-mcp-server/
├── 📄 main.py                      # Enhanced MCP server (1279 lines)
│   ├── 🧠 Smart movie discovery tools
│   ├── 🌐 Multi-language support (15+ languages)
│   ├── 📊 Automatic metadata enrichment
│   ├── ⚡ Never-repeat logic
│   └── 🎯 Quick rating system
│
├── 📄 generate_movie_display.py    # Static HTML generator (681 lines)
│   ├── 🖼️ Jinja2 template system
│   ├── 🌐 Language filtering
│   ├── 📱 Responsive design
│   └── ⭐ Beautiful movie cards
│
├── 📄 my_reviews.json             # Enhanced review storage
│   ├── 📊 Rich metadata per movie
│   ├── 🖼️ Poster URLs
│   ├── 🔗 IMDb links
│   └── 🌐 Language tags
│
├── 🗂️ movie_display/              # Generated web files
│   ├── 📄 index.html             # All movies gallery
│   ├── 📄 index_hindi.html       # Hindi movies only
│   ├── 📄 index_english.html     # English movies only
│   └── 📄 index_[language].html  # Per-language galleries
│
├── 📄 movie_reviews_display.py    # Flask version (alternative)
├── 🗂️ templates/                  # Flask templates
│   └── 📄 movie_reviews.html     # Flask template file
│
├── 📄 requirements.txt           # Dependencies (includes Jinja2)
├── 📄 README.md                 # This comprehensive guide
├── 📄 CLARIFICATIONS.md         # OMDb vs IMDb clarifications
├── 📄 .env                      # OMDb API key configuration
└── 📄 .gitignore               # Git ignore patterns
```

## 🚀 Installation

### Prerequisites

- **Python 3.9+** 
- **Claude Desktop** or **Cursor IDE**
- **OMDb API Key** (free from [omdbapi.com](http://www.omdbapi.com/apikey.aspx))

### Quick Setup

```bash
# 1. Navigate to workspace
cd ~/workspace
git clone <your-repo> imdb-mcp-server
cd imdb-mcp-server

# 2. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
echo "OMDB_API_KEY=your_actual_api_key_here" > .env

# 5. Generate initial web display
python generate_movie_display.py
```

### Claude Desktop Configuration

Edit `~/.config/claude-desktop/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "movie-review-server": {
      "command": "/path/to/imdb-mcp-server/venv/bin/python",
      "args": ["/path/to/imdb-mcp-server/main.py"],
      "cwd": "/path/to/imdb-mcp-server",
      "env": {
        "PYTHONPATH": "/path/to/imdb-mcp-server/venv/lib/python3.13/site-packages"
      }
    }
  }
}
```

**Restart Claude Desktop** to load the enhanced server.

## 🛠️ Available Tools

### 🧠 Smart Discovery Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `start_movie_discussion_session()` | None | Initiate intelligent movie discussion |
| `discover_movies_by_criteria()` | `language, year_start, year_end, count` | Find movies by language/era (excludes reviewed) |
| `get_unreviewed_movies_count()` | `language, year_start, year_end` | Count undiscovered movies |

### ⚡ Quick Review Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `quick_rate_movie()` | `title, rating, review` | Streamlined rating during discussions |
| `write_review()` | `title, rating, review` | Full review with metadata enrichment |

### 📊 Enhanced Review Management

| Tool | Parameters | Description |
|------|------------|-------------|
| `search_movie()` | `title` | Search movie data via OMDb API |
| `get_review()` | `title` | Retrieve review with rich metadata |
| `list_reviews()` | None | List all reviews with statistics |
| `delete_review()` | `title` | Delete a movie review |
| `get_top_rated_movies()` | `limit` | Get highest-rated movies |

### 📤 Export & Display Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `export_review_for_posting()` | `title` | Export single review (multiple formats) |
| `export_all_reviews()` | None | Export all reviews with instructions |
| **Web Display** | `generate_movie_display.py` | Generate beautiful HTML galleries |

## 🧠 Smart Discussion System

### Starting a Discussion Session

```
User: "Let's discuss movies"
Claude: "What language and time period would you like to explore?"
User: "2000s Hindi movies"
Claude: "Great! Let me discover some 2000s Hindi cinema for you..."
```

### How It Works

1. **Language Detection** - Recognizes 15+ languages
2. **Era Filtering** - Searches within specified year range  
3. **Smart Keywords** - Uses culturally relevant search terms:
   - **Hindi**: "Bollywood", "Aamir Khan", "Shah Rukh Khan", "Mumbai"
   - **Korean**: "Seoul", "K-drama", "Korean cinema"
   - **Japanese**: "Tokyo", "anime", "Japanese film"
4. **Never Repeat** - Automatically excludes already-reviewed movies
5. **Batch Discovery** - Finds multiple movies per session
6. **Quick Rating** - Streamlined review process during discussions

### Example Session Flow

```
🎬 Discovered: "Dil Chahta Hai" (2001)
⭐ IMDb Rating: 8.1/10
🎭 Genre: Comedy, Drama, Romance  
🎬 Director: Farhan Akhtar

Have you watched this movie? If yes, how would you rate it (1-10)?
```

## 🌐 Multi-Language Support

### Supported Languages & Search Strategy

Each language uses **culturally relevant keywords** for better discovery:

| Language | Keywords Used | Example Actors/Terms |
|----------|---------------|----------------------|
| **Hindi** | Bollywood, Mumbai, Aamir Khan, Shah Rukh Khan | Lagaan, 3 Idiots |
| **English** | Hollywood, British, American cinema | Inception, The Matrix |
| **Korean** | Seoul, K-drama, Korean cinema | Parasite, Train to Busan |
| **Japanese** | Tokyo, anime, Japanese film | Spirited Away, Your Name |
| **Spanish** | Madrid, Barcelona, Spanish cinema | Pan's Labyrinth, Volver |
| **French** | Paris, French cinema, Cannes | Amélie, The Artist |
| **Tamil** | Chennai, Kollywood, Tamil cinema | Enthiran, 96 |
| **Telugu** | Tollywood, Hyderabad | Baahubali, RRR |

### Language-Specific Features

- **Smart Actor Recognition** - Searches using popular actors from each language
- **Cultural Keywords** - Uses region-specific cinema terms
- **Era Context** - Understands different cinematic periods per language
- **Genre Preferences** - Recognizes popular genres per culture

## 🖼️ Web Display Generation

### Generated Files

The `generate_movie_display.py` script creates:

- **`movie_display/index.html`** - All movies in beautiful gallery
- **`movie_display/index_[language].html`** - Language-specific galleries
- **Navigation Links** - Easy switching between languages
- **Statistics Dashboard** - Total movies, ratings, languages

### Features

```html
🎬 Beautiful Movie Cards
├── 🖼️ Movie Poster Images
├── ⭐ Star Rating Display (★★★★☆)
├── 📅 Year Prominently Displayed  
├── 🌐 Language Badge
├── 🔗 Direct IMDb Links
├── 📊 IMDb Rating Reference
├── 📝 Review Text
└── 📅 Review Date
```

### Usage

```bash
# Generate/update web display
python generate_movie_display.py

# Open in browser
open movie_display/index.html
```

### Design Features

- **📱 Responsive Design** - Beautiful on all devices
- **🎨 Modern UI** - Gradient backgrounds, hover effects
- **⚡ Fast Loading** - Static HTML, no server required
- **🌐 Language Navigation** - Quick filtering by language
- **📊 Statistics** - Overview of your collection
- **🔗 Direct Links** - One-click access to IMDb pages

## 📊 Enhanced Review System

### Rich Metadata Structure

Each review now includes comprehensive metadata:

```json
{
  "Movie Title": {
    "rating": 8,
    "review": "Amazing cinematography and storyline!",
    "date_added": "2024-06-09T19:15:00",
    "last_updated": "2024-06-09T19:15:00",
    "imdb_link": "https://www.imdb.com/title/tt1375666/",
    "poster_url": "https://m.media-amazon.com/images/...",
    "imdb_id": "tt1375666",
    "year": "2010",
    "director": "Christopher Nolan",
    "genre": "Action, Sci-Fi, Thriller",
    "imdb_rating": "8.8",
    "language": "English",
    "country": "USA, UK"
  }
}
```

### Automatic Enrichment

When you write any review, the system automatically:

1. **Fetches OMDb Data** - Gets comprehensive movie information
2. **Extracts Poster URL** - High-quality movie poster image
3. **Generates IMDb Link** - Direct link to IMDb page
4. **Stores Rich Metadata** - Director, genre, language, country, IMDb rating
5. **Maintains Timestamps** - Creation and modification tracking

### Display Features

- **📅 Year Prominently Displayed** - Always visible in reviews
- **🌐 Language Prominently Displayed** - Clear language identification
- **⭐ Star Visualization** - Beautiful ★★★★★ representation
- **🎬 Director Information** - Filmmaker details
- **🎭 Genre Tags** - Movie classification
- **📊 IMDb Rating Reference** - Official rating alongside yours

## 📤 Export Functionality

### Multiple Export Formats

- **IMDb Ready** - Formatted for IMDb review section
- **Letterboxd Ready** - Optimized for Letterboxd
- **Markdown** - For blogs and documentation  
- **Social Media** - Twitter/Facebook/Instagram ready
- **Web Display** - Beautiful HTML galleries

### Export Features

- **Rich Metadata** - Includes all movie information
- **Multiple Platforms** - Platform-specific formatting
- **Batch Export** - All reviews at once
- **Manual Posting** - Copy-paste instructions included

**⚠️ Important:** All posting to external platforms (IMDb, Letterboxd) must be done manually via copy-paste.

## 🔧 Troubleshooting

### Common Issues

#### Web Display Not Generating
```bash
# Check for Jinja2
pip install Jinja2>=3.1.0

# Run generator
python generate_movie_display.py
```

#### Missing Movie Posters
- OMDb API may not have poster for some movies
- System gracefully handles missing posters with placeholders

#### Language Not Recognized
- Currently supports 15+ languages
- Add new languages by updating the `LANGUAGE_KEYWORDS` dictionary in `main.py`

#### Smart Discovery Not Working
- Check OMDb API key and quota (1,000 requests/day free)
- Verify internet connection
- Some languages may have limited movie data in OMDb

### Testing Enhanced Features

```bash
# Test smart discovery
python -c "from main import discover_movies_by_criteria; print(discover_movies_by_criteria('Hindi', 2000, 2010, 5))"

# Test metadata enrichment  
python -c "from main import fetch_movie_metadata; print(fetch_movie_metadata('Inception'))"

# Test web generation
python generate_movie_display.py
```

## 🤝 Contributing

### Development Areas

- **🌐 Language Support** - Add more languages and cultural keywords
- **🎨 Web Design** - Enhance HTML templates and styling
- **📊 Analytics** - Add more statistical analysis features
- **🔍 Discovery** - Improve smart movie discovery algorithms
- **📱 Mobile** - Enhance mobile responsiveness

### Code Guidelines

- Follow existing patterns for multi-language support
- Add comprehensive docstrings for all functions
- Test new features with multiple languages
- Ensure backward compatibility with existing reviews
- Update documentation for new features

---

## 🎬 Usage Examples

### Smart Movie Discussion
```
"Let's discuss 2000s Korean movies"
→ Discovers Korean cinema, asks if you've watched each, collects ratings
```

### Quick Rating During Discovery
```
"Rate Parasite 9/10 - Masterpiece of social commentary"
→ Automatically enriches with metadata, saves review
```

### Generate Beautiful Web Display
```bash
python generate_movie_display.py
→ Creates stunning HTML galleries with posters and metadata
```

### Language-Specific Browsing
```
Open movie_display/index_korean.html
→ View only Korean movies with posters and IMDb links
```

**🎉 Happy movie reviewing with intelligence and style! 🎬✨**

*Enhanced MCP server with smart discovery, rich metadata, and beautiful web displays - all while maintaining manual posting requirements for external platforms.* 
