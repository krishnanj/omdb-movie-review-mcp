# 🎬 Movie Review MCP Server (OMDb + Personal Reviews)

A powerful Model Context Protocol (MCP) server that enables AI assistants to search movies via **OMDb API** and manage your personal movie reviews with both quantitative ratings and qualitative text reviews.

**⚠️ Important:** This server uses the **OMDb (Open Movie Database) API** for movie data, not direct IMDb access. While it can export reviews formatted for IMDb, **it cannot automatically post to IMDb** - all posting must be done manually.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [File Structure](#file-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Tools](#available-tools)
- [Review System](#review-system)
- [Export Functionality](#export-functionality)
- [API Limitations](#api-limitations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

- **🔍 Movie Search**: Search movies using the **OMDb API** (Open Movie Database)
- **⭐ Rating System**: Rate movies on a 1-10 scale (stored locally)
- **📝 Text Reviews**: Write detailed qualitative reviews (stored locally)
- **📊 Analytics**: Get top-rated movies and average ratings
- **📤 Export Reviews**: Export reviews formatted for manual posting to IMDb, Letterboxd, blogs, etc.
- **🔄 Backward Compatibility**: Supports legacy text-only reviews
- **📅 Timestamps**: Track when reviews were added/updated

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Desktop / Cursor                  │
│                      (MCP Host)                            │
└─────────────────────┬───────────────────────────────────────┘
                      │ JSON-RPC over stdio
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Movie Review MCP Server                       │
│                   (main.py)                               │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              FastMCP Framework                      │  │
│  │                                                     │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │   OMDb      │  │   Local     │  │   Export    │ │  │
│  │  │   Search    │  │   Reviews   │  │   Tools     │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────┬──────────────┬────────────────────────┘
                      │              │
        ┌─────────────▼─┐          ┌─▼──────────────┐
        │   OMDb API    │          │  Local JSON    │
        │  (Read-Only)  │          │  Reviews File  │
        │   External    │          │  (Read/Write)  │
        └───────────────┘          └─────────────────┘
```

**Data Flow:**
- **Movie Info**: OMDb API → Server → Claude Desktop (read-only)
- **Reviews**: Local JSON ← Server ← Claude Desktop (read/write)
- **Export**: Local JSON → Formatted text → Manual posting to platforms

## 📁 File Structure

```
movie-review-mcp-server/
├── 📄 main.py                 # Main MCP server implementation
├── 📄 README.md              # This documentation file
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env                   # Environment variables (OMDb API key)
├── 📄 .gitignore            # Git ignore patterns
├── 📄 my_reviews.json       # Your movie reviews (auto-generated)
├── 🗂️ tools/                # Legacy tool modules (optional)
│   ├── 📄 omdb.py           # OMDb search functionality
│   └── 📄 reviews.py        # Review management functions
├── 🗂️ venv/                 # Python virtual environment
└── 🗂️ __pycache__/          # Python bytecode cache
```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- Claude Desktop or Cursor IDE
- **OMDb API key** (free from [omdbapi.com](http://www.omdbapi.com/apikey.aspx))

### Step 1: Clone and Setup

```bash
# Navigate to your workspace
cd ~/workspace

# Clone or create the directory
mkdir movie-review-mcp-server
cd movie-review-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get OMDb API Key

1. Visit [OMDb API](http://www.omdbapi.com/apikey.aspx)
2. Sign up for a free API key
3. Save your key for the next step

**Note:** OMDb is a third-party service that provides IMDb data via API. It's not affiliated with IMDb directly.

### Step 3: Configure Environment

```bash
# Create .env file
echo "OMDB_API_KEY=your_actual_api_key_here" > .env
```

### Step 4: Add to Claude Desktop

Edit `~/.config/claude-desktop/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "movie-review-server": {
      "command": "/path/to/your/movie-review-mcp-server/venv/bin/python",
      "args": ["/path/to/your/movie-review-mcp-server/main.py"],
      "cwd": "/path/to/your/movie-review-mcp-server",
      "env": {
        "PYTHONPATH": "/path/to/your/movie-review-mcp-server/venv/lib/python3.13/site-packages"
      }
    }
  }
}
```

### Step 5: Restart Claude Desktop

Completely quit and restart Claude Desktop to load the MCP server.

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OMDB_API_KEY` | Yes | Your OMDb API key for movie searches |

### Claude Desktop Settings

The server uses `stdio` transport and runs as a subprocess of Claude Desktop. Ensure the paths in your configuration match your actual installation directory.

## 📖 Usage

Once configured, you can interact with the server through natural language in Claude Desktop:

### Movie Search Examples (via OMDb)
```
"Search for the movie Inception"
"Find details about The Dark Knight"
"Look up Pulp Fiction"
```

### Writing Reviews Examples (stored locally)
```
"Write a review for Inception with rating 9 and text 'Mind-bending masterpiece with incredible visuals'"
"Rate The Matrix 10 out of 10 and review it as 'Revolutionary sci-fi classic'"
"Add a review for Titanic: rating 7, review 'Epic romance but overly long'"
```

### Reading Reviews Examples (from local storage)
```
"What did I think about Inception?"
"Show me my review for The Dark Knight"
"What are all my movie reviews?"
"What are my top 5 rated movies?"
```

### Export Examples (for manual posting)
```
"Export my Inception review for posting to IMDb"
"Export all my reviews in different formats"
"Prepare my Matrix review for Letterboxd"
```

## 🛠️ Available Tools

### Core Tools

| Tool | Parameters | Description | Data Source |
|------|------------|-------------|-------------|
| `search_movie` | `title: str` | Search for movie data | OMDb API (read-only) |
| `write_review` | `title: str, rating: int, review: str` | Write/update movie review | Local JSON file |
| `get_review` | `title: str` | Retrieve your review | Local JSON file |
| `list_reviews` | None | List all reviews with statistics | Local JSON file |
| `delete_review` | `title: str` | Delete a movie review | Local JSON file |
| `get_top_rated_movies` | `limit: int = 5` | Get your highest-rated movies | Local JSON file |

### Export Tools

| Tool | Parameters | Description | Output |
|------|------------|-------------|--------|
| `export_review_for_posting` | `title: str` | Export single review in multiple formats | Formatted text for manual posting |
| `export_all_reviews` | None | Export all reviews with posting instructions | Formatted text for manual posting |

## 📊 Review System

### Review Structure

Each review contains:

```json
{
  "movie_title": {
    "rating": 8,
    "review": "Amazing cinematography and storyline!",
    "date_added": "2024-06-09T19:15:00",
    "last_updated": "2024-06-09T19:15:00"
  }
}
```

### Rating Scale

- **1-3**: Poor/Disliked
- **4-6**: Average/Mixed feelings  
- **7-8**: Good/Enjoyed
- **9-10**: Excellent/Loved

### Features

- **Quantitative Ratings**: 1-10 integer scale
- **Qualitative Reviews**: Detailed text feedback
- **Timestamps**: Creation and modification dates
- **Statistics**: Average ratings, top movies
- **Backward Compatibility**: Supports old text-only reviews

## 📤 Export Functionality

### ⚠️ Important Limitations

**This server CANNOT automatically post to IMDb or other platforms.** All exports are formatted text that you must manually copy and paste to the target platform.

### Supported Export Formats

- **IMDb Ready**: Formatted for copy-paste to IMDb review section
- **Letterboxd Ready**: Optimized for Letterboxd platform
- **Markdown**: For blogs and documentation
- **Social Media**: For Twitter, Facebook, Instagram posts

### Export Features

- **Star Ratings**: Visual ★★★★★ representation
- **Movie Metadata**: Includes OMDb data when available
- **Direct Links**: IMDb URLs for easy navigation
- **Batch Export**: Export all reviews at once
- **Platform Instructions**: Clear guidance for manual posting

### Manual Posting Process

1. **Export**: Use export tools to get formatted text
2. **Copy**: Copy the appropriate format for your target platform
3. **Navigate**: Go to the movie page on IMDb/Letterboxd/etc.
4. **Paste**: Manually paste your review content
5. **Submit**: Complete the posting process on the platform

## 🚫 API Limitations

### What This Server CAN Do:
- ✅ Search movie information via OMDb API
- ✅ Store and manage your personal reviews locally
- ✅ Export reviews in various formats
- ✅ Provide movie metadata (title, year, cast, plot, etc.)
- ✅ Generate formatted text for manual posting

### What This Server CANNOT Do:
- ❌ Post reviews directly to IMDb
- ❌ Post reviews directly to Letterboxd
- ❌ Access your IMDb account
- ❌ Modify data on any external movie platform
- ❌ Access real-time IMDb ratings/reviews from other users

### Why These Limitations Exist:
- **OMDb API**: Read-only access to movie data, no write capabilities
- **IMDb API**: No public API for posting reviews
- **Letterboxd API**: No public API for posting reviews
- **Security**: External platforms don't allow automated posting for security reasons

### Alternative Platforms with APIs:
- **Twitter**: Can post review tweets via API
- **Reddit**: Can post to movie subreddits via API
- **Personal Blog**: Full control over your own platform

## 🔧 Troubleshooting

### Common Issues

#### Server Not Appearing in Claude Desktop

1. **Check configuration path**: Ensure absolute paths in config
2. **Restart Claude**: Completely quit and restart
3. **Check logs**: Look for MCP server errors
4. **Verify permissions**: Ensure execute permissions on Python

#### Permission Denied Errors

1. **Check file permissions**: Ensure write access to directory
2. **Verify paths**: Confirm all paths exist and are accessible
3. **Environment variables**: Ensure `.env` file is readable

#### OMDb API Errors

1. **Verify API key**: Check `.env` file has correct key
2. **Check quota**: Free tier has daily limits (1,000 requests/day)
3. **Network issues**: Ensure internet connectivity
4. **Rate limiting**: OMDb may throttle requests if too frequent

#### Export/Posting Issues

1. **Format compatibility**: Different platforms have different requirements
2. **Character limits**: Some platforms limit review length
3. **Manual posting required**: Remember - no automatic posting is possible

### Testing the Server

```bash
# Test OMDb connection
source venv/bin/activate
python -c "from main import search_movie; print(search_movie('Inception'))"

# Test local reviews
python -c "from main import list_reviews; print(list_reviews())"
```

### Debug Mode

Enable detailed logging by modifying the server startup:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Add type hints for function parameters
- Include docstrings for all functions
- Write descriptive commit messages
- Clearly distinguish between OMDb API calls and local operations

### Testing

```bash
# Run the test script
python test_new_reviews.py
```

## 📄 License

This project is open source. Feel free to use, modify, and distribute as needed.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section
2. Verify your OMDb API key and quota
3. Test the server directly
4. Check Claude Desktop logs
5. Remember: All posting to external platforms must be done manually

---

**Happy movie reviewing! 🎬✨**

*This server uses OMDb API for movie data and stores your reviews locally. Manual posting to IMDb and other platforms required.* 