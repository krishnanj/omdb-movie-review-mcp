# 🔍 OMDb vs IMDb Clarifications

## Important Distinctions

### What This Server Uses: OMDb API
- **OMDb** = Open Movie Database
- **Third-party service** that provides IMDb data via API
- **Read-only access** to movie information
- **NOT affiliated** with IMDb directly
- **Free tier**: 1,000 requests per day

### What This Server Does NOT Use: Direct IMDb Access
- **No direct IMDb API** (IMDb doesn't provide public write API)
- **Cannot post** reviews to IMDb automatically
- **Cannot access** your IMDb account
- **Cannot modify** any data on IMDb

## 🚫 Limitations Summary

### ✅ What We CAN Do:
- Search movie information via OMDb API
- Store your personal reviews locally
- Export reviews in various formats
- Generate formatted text for posting
- Provide movie metadata (title, year, cast, plot, etc.)

### ❌ What We CANNOT Do:
- Post reviews directly to IMDb
- Post reviews directly to Letterboxd  
- Access your IMDb/Letterboxd accounts
- Modify data on any external platform
- Get real-time user reviews from IMDb

## 📤 Export vs Automatic Posting

### Export Functions:
- Generate **formatted text only**
- Provide **copy-paste ready** content
- Include **platform-specific formatting**
- Offer **posting instructions**

### Manual Posting Required:
1. **Export** your review using the tools
2. **Copy** the appropriate format
3. **Navigate** to IMDb/Letterboxd manually
4. **Paste** your review content
5. **Submit** through the platform's interface

## 🔄 Data Flow

```
Movie Search:
OMDb API → Server → Formatted Display

Review Management:
Your Input → Server → Local JSON File

Export Process:
Local JSON → Server → Formatted Text → Manual Copy/Paste → External Platform
```

## 📡 OMDb API Details

### What OMDb Provides:
- Movie titles, years, cast, crew
- Plot summaries and genres
- IMDb ratings and vote counts
- Box office information
- Awards and technical details
- IMDb IDs and direct links

### OMDb Limitations:
- **Read-only** data access
- **No write capabilities**
- **May not reflect** real-time IMDb changes
- **Rate limited** (1,000 requests/day free tier)
- **No user-generated content** (reviews, lists, etc.)

## 💾 Local Storage Benefits

### Why Store Locally:
- **Full control** over your data
- **No platform restrictions**
- **Backup and export** capabilities
- **Privacy protection**
- **Offline access** to your reviews

### Local Storage Features:
- JSON format for easy reading
- Timestamps for tracking changes
- Rating scales customizable
- Backward compatibility
- Easy migration/export

## 🔗 Platform Integration Guide

### IMDb Integration:
1. Use export tools to get formatted review
2. Go to movie page on IMDb
3. Click "Write a Review"
4. Copy/paste your rating and text
5. Submit through IMDb's interface

### Letterboxd Integration:
1. Export review in Letterboxd format
2. Search movie on Letterboxd
3. Add to "Watched" list
4. Copy/paste star rating and text
5. Save through Letterboxd interface

### Blog Integration:
1. Export in Markdown format
2. Copy entire formatted content
3. Paste into your blog editor
4. Customize styling as needed
5. Publish on your platform

## ⚡ Quick Reference

| Feature | Status | Method |
|---------|--------|--------|
| Movie Search | ✅ Available | OMDb API (read-only) |
| Review Storage | ✅ Available | Local JSON (read/write) |
| Review Export | ✅ Available | Formatted text generation |
| IMDb Posting | ❌ Manual Only | Copy/paste exported text |
| Letterboxd Posting | ❌ Manual Only | Copy/paste exported text |
| Account Access | ❌ Not Available | No platform APIs available |

## 🛠️ Technical Implementation

### Server Architecture:
```
Claude Desktop
    ↓ JSON-RPC
MCP Server
    ↓ HTTP (read-only)
OMDb API
```

### Review Management:
```
User Input
    ↓ Validation
Local JSON Storage
    ↓ Export Tools
Formatted Text Output
```

This clarifies that our server is a **movie review management tool** that uses OMDb for movie data and requires manual posting to external platforms. 