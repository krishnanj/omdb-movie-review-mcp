# 🏗️ Enhanced Movie Review MCP Server - Architecture Documentation

## 📊 System Overview

The Enhanced Movie Review MCP Server is a comprehensive platform that combines intelligent movie discovery, automatic metadata enrichment, and beautiful web displays. This document provides detailed technical architecture and implementation details.

## 🎯 Core Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           User Interface Layer                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │ Claude Desktop  │  │   Cursor IDE    │  │    Generated Web Display    │ │
│  │   (Primary)     │  │  (Alternative)  │  │     (Static HTML)           │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                           JSON-RPC over stdio
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Enhanced MCP Server Core                             │
│                              (main.py)                                     │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      FastMCP Framework                              │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐  │   │
│  │  │ Smart Discovery │ │ Enhanced Review │ │  Export & Display   │  │   │
│  │  │    Engine       │ │   Management    │ │     Generator       │  │   │
│  │  │                 │ │                 │ │                     │  │   │
│  │  │• Language AI    │ │• Metadata Auto  │ │• Multi-Format Export│  │   │
│  │  │• Era Filtering  │ │• Timestamp Track│ │• HTML Generation    │  │   │
│  │  │• Never Repeat   │ │• Rich Storage   │ │• Language Filtering │  │   │
│  │  │• Cultural Keys  │ │• Star Display   │ │• Static Web Files   │  │   │
│  │  └─────────────────┘ └─────────────────┘ └─────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                            │                              │
                    ┌───────▼────────┐                     │
                    │   OMDb API     │                     │
                    │   Integration  │                     │
                    │                │                     │
                    │• Movie Search  │                     │
                    │• Metadata      │                     │
                    │• Poster URLs   │                     │
                    │• IMDb IDs      │                     │
                    │• Multi-Lang    │                     │
                    └────────────────┘                     │
                                                           │
┌─────────────────────────────────────────────────────────▼─────────────────┐
│                           Data Storage Layer                              │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                    Enhanced JSON Reviews                            │  │
│  │                      (my_reviews.json)                             │  │
│  │                                                                     │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │  │
│  │  │Legacy Review│ │Rich Metadata│ │Poster Images│ │IMDb Links   │  │  │
│  │  │Support      │ │Integration  │ │Storage      │ │Generation   │  │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────┘
                                          │
                                          │
┌─────────────────────────────────────────▼─────────────────────────────────┐
│                        Web Display Generation                             │
│                     (generate_movie_display.py)                          │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                     Jinja2 Template Engine                         │  │
│  │                                                                     │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │  │
│  │  │Language     │ │Responsive   │ │Poster       │ │Statistics   │  │  │
│  │  │Detection    │ │Design       │ │Integration  │ │Dashboard    │  │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                     │                                     │
│                                     ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                   Static HTML Gallery Files                        │  │
│  │                                                                     │  │
│  │  index.html          │  index_hindi.html   │  index_english.html    │  │
│  │  (All Movies)        │  (Hindi Only)       │  (English Only)        │  │
│  │                      │                     │                        │  │
│  │  index_korean.html   │  index_spanish.html │  [Additional Languages]│  │
│  │  (Korean Only)       │  (Spanish Only)     │  (Based on Collection) │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────┘
```

## 🧠 Smart Discovery Engine Architecture

### Language Processing Pipeline
```
User Request
    │
    ▼
Language Detection
    │
    ▼
Cultural Keywords Mapping
    │
    ▼
Era/Year Filtering
    │
    ▼
OMDb API Search Strategy
    │
    ▼
Never-Repeat Logic
    │
    ▼
Result Presentation
```

### Language Keywords System
```python
LANGUAGE_KEYWORDS = {
    "hindi": {
        "actors": ["Aamir Khan", "Shah Rukh Khan", "Salman Khan"],
        "locations": ["Mumbai", "Bollywood"],
        "genres": ["Bollywood", "Hindi cinema"]
    },
    "korean": {
        "actors": ["Song Kang-ho", "Park So-dam"],
        "locations": ["Seoul", "Korea"],
        "genres": ["K-drama", "Korean cinema"]
    },
    # ... 15+ languages supported
}
```

## 📊 Enhanced Review Management System

### Data Model Evolution
```
Legacy Format (v1.0):
{
    "Movie Title": "Simple review text string"
}

Enhanced Format (v2.0):
{
    "Movie Title": {
        "rating": 8,
        "review": "Detailed review text",
        "date_added": "2024-06-09T19:15:00",
        "last_updated": "2024-06-09T19:15:00",
        "imdb_link": "https://www.imdb.com/title/...",
        "poster_url": "https://m.media-amazon.com/...",
        "imdb_id": "tt1234567",
        "year": "2010",
        "director": "Christopher Nolan",
        "genre": "Action, Sci-Fi, Thriller",
        "imdb_rating": "8.8",
        "language": "English",
        "country": "USA, UK"
    }
}
```

### Metadata Enrichment Flow
```
Movie Title Input
    │
    ▼
OMDb API Query
    │
    ▼
Metadata Extraction
    ├── Poster URL
    ├── IMDb ID → IMDb Link
    ├── Director & Genre
    ├── Language & Country
    └── IMDb Rating
    │
    ▼
Enhanced JSON Storage
    │
    ▼
Backward Compatibility Check
    │
    ▼
Final Review Object
```

## 🖼️ Web Display Generation Architecture

### Template System Architecture
```
Enhanced JSON Reviews
    │
    ▼
Language Detection & Separation
    │
    ▼
Jinja2 Template Processing
    ├── Main Template (All Movies)
    ├── Language-Specific Templates
    └── Statistical Calculations
    │
    ▼
Static HTML Generation
    ├── index.html (Main Gallery)
    ├── index_[lang].html (Filtered)
    └── Navigation Links
    │
    ▼
Responsive CSS Injection
    ├── Mobile Optimized
    ├── Desktop Enhanced
    └── Tablet Adapted
    │
    ▼
Final Web Gallery Files
```

### Responsive Design System
```css
/* Mobile First Approach */
.movies-grid {
    grid-template-columns: 1fr;                    /* Mobile: Single column */
}

@media (min-width: 768px) {
    .movies-grid {
        grid-template-columns: repeat(2, 1fr);     /* Tablet: Two columns */
    }
}

@media (min-width: 1200px) {
    .movies-grid {
        grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));  /* Desktop: Flexible grid */
    }
}
```

## 🔄 Data Flow Diagrams

### Smart Discussion Workflow
```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Smart Discussion Flow                             │
└─────────────────────────────────────────────────────────────────────────┘

User Input: "Let's discuss 2000s Hindi movies"
    │
    ▼
start_movie_discussion_session()
    │
    ▼
Language & Era Extraction
    │ ("Hindi", 2000-2009)
    ▼
discover_movies_by_criteria("Hindi", 2000, 2009, 10)
    │
    ▼
Cultural Keywords Application
    │ ("Bollywood", "Aamir Khan", "Mumbai")
    ▼
OMDb API Search Loop
    │
    ▼
Never-Repeat Filtering
    │ (Exclude already reviewed movies)
    ▼
Movie Presentation with Metadata
    │ (Title, Year, Director, IMDb Rating)
    ▼
User Rating Collection
    │
    ▼
quick_rate_movie() OR write_review()
    │
    ▼
Automatic Metadata Enrichment
    │ (Poster, IMDb Link, Rich Data)
    ▼
Enhanced JSON Storage
    │
    ▼
Optional: generate_movie_display.py
    │
    ▼
Beautiful Web Gallery Update
```

### Export & Display Generation Flow
```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Export & Display Generation                          │
└─────────────────────────────────────────────────────────────────────────┘

Enhanced JSON Reviews
    │
    ├─────────────────────────────────┬─────────────────────────────────┐
    │                                 │                                 │
    ▼                                 ▼                                 ▼
Export Tools                    Web Display Generator          Manual Sharing
    │                                 │                                 │
    ▼                                 ▼                                 ▼
export_review_for_posting()     generate_movie_display.py        Copy/Paste to:
export_all_reviews()                  │                           ├── IMDb
    │                                 ▼                           ├── Letterboxd
    ▼                           Language Detection                ├── Social Media
Multiple Formats:                     │                           └── Blogs
├── IMDb Ready                        ▼                                 │
├── Letterboxd Ready            Static HTML Generation                  ▼
├── Markdown                          │                           Manual Posting
├── Social Media                      ▼                           (External Platforms)
└── Plain Text                 Beautiful Web Galleries
                                      │
                                      ▼
                               Self-Hosted Sharing
                               (Upload HTML files)
```

## 🛠️ Technical Implementation Details

### MCP Tool Architecture
```python
# Tool Categories and Organization

@mcp.tool()  # Smart Discovery Tools
def start_movie_discussion_session() -> str
def discover_movies_by_criteria(language, year_start, year_end, count) -> str
def get_unreviewed_movies_count(language, year_start, year_end) -> str

@mcp.tool()  # Enhanced Review Management
def quick_rate_movie(title, rating, review) -> str
def write_review(title, rating, review) -> str
def get_review(title) -> str
def list_reviews() -> str
def delete_review(title) -> str
def get_top_rated_movies(limit) -> str

@mcp.tool()  # Core Movie Search
def search_movie(title) -> str

@mcp.tool()  # Export & Display
def export_review_for_posting(title) -> str
def export_all_reviews() -> str

# External Tool (Standalone)
# python generate_movie_display.py
```

### Language Support Implementation
```python
# Multi-Language Cinema Support
LANGUAGE_KEYWORDS = {
    "hindi": {
        "keywords": ["Bollywood", "Mumbai", "Hindi cinema"],
        "actors": ["Aamir Khan", "Shah Rukh Khan", "Salman Khan", "Amitabh Bachchan"],
        "directors": ["Raj Kapoor", "Yash Chopra"],
        "regions": ["Mumbai", "Delhi", "India"]
    },
    "korean": {
        "keywords": ["K-drama", "Korean cinema", "Seoul"],
        "actors": ["Song Kang-ho", "Park So-dam", "Choi Min-sik"],
        "directors": ["Bong Joon-ho", "Park Chan-wook"],
        "regions": ["Seoul", "Korea", "Korean"]
    },
    # ... extends to 15+ languages
}
```

### Web Generation Pipeline
```python
# HTML Generation Process
def generate_html_files():
    reviews = load_reviews()                    # Load enhanced JSON
    languages = get_languages(reviews)         # Detect languages
    
    # Generate main page (all movies)
    all_movies = prepare_movie_data(reviews)
    generate_html_page("index.html", all_movies, "all")
    
    # Generate language-specific pages
    for language in languages:
        filtered_movies = prepare_movie_data(reviews, language)
        safe_lang = language.replace(" ", "_").lower()
        generate_html_page(f"index_{safe_lang}.html", filtered_movies, language)
```

## 📊 Performance and Scalability

### OMDb API Usage Optimization
- **Rate Limiting**: 1,000 requests/day (free tier)
- **Caching**: Metadata stored locally to avoid re-requests
- **Batch Processing**: Smart discovery fetches multiple movies efficiently
- **Error Handling**: Graceful degradation when API limits reached

### Web Display Performance
- **Static Generation**: No server-side processing required
- **Embedded CSS**: Self-contained HTML files
- **Image Optimization**: Lazy loading for poster images
- **Mobile Optimization**: Responsive grid system

### Storage Efficiency
- **JSON Format**: Human-readable and easily parseable
- **Backward Compatibility**: Legacy reviews coexist with enhanced ones
- **Incremental Updates**: Only modified reviews trigger regeneration

## 🔐 Security Considerations

### API Key Management
- Environment variable storage (`.env` file)
- No hardcoded API keys in source code
- Local-only storage (no cloud dependencies)

### Data Privacy
- All review data stored locally
- No automatic posting to external platforms
- User maintains full control over data

### Web Display Security
- Static HTML only (no server-side code)
- No user input processing in generated files
- Safe for local hosting or static file sharing

## 🧪 Testing and Quality Assurance

### Component Testing
```bash
# Test smart discovery
python -c "from main import discover_movies_by_criteria; print(discover_movies_by_criteria('Hindi', 2000, 2010, 5))"

# Test metadata enrichment
python -c "from main import fetch_movie_metadata; print(fetch_movie_metadata('Inception'))"

# Test web generation
python generate_movie_display.py

# Test review management
python -c "from main import list_reviews; print(list_reviews())"
```

### Integration Testing
- OMDb API connectivity verification
- JSON schema validation
- HTML generation verification
- Cross-browser compatibility testing

## 🚀 Future Architecture Considerations

### Planned Enhancements
- **Additional Languages**: Expand beyond 15 current languages
- **Advanced Analytics**: Movie trends, genre preferences
- **Enhanced Discovery**: Machine learning for recommendations
- **Export Formats**: Additional platforms and formats
- **Mobile App**: Native mobile interface

### Scalability Improvements
- **Database Option**: SQLite for large collections
- **Cloud Storage**: Optional cloud backup integration
- **API Caching**: Redis for improved performance
- **Batch Processing**: Background job system for large operations

This architecture provides a comprehensive foundation for intelligent movie review management while maintaining simplicity, privacy, and user control. 