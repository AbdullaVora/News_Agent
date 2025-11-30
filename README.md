# 🤖 Smart News Aggregator - Multi-Agent AI System

A sophisticated news aggregation platform powered by **6 specialized AI agents** working together to deliver intelligent, ranked, and summarized news from multiple sources.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)

---

## ✨ Features

### **Multi-Agent Architecture**
- **6 Specialized Agents** working in parallel
- **Fault-tolerant** design with fallback mechanisms
- **Real-time metrics** for each agent
- **Production-grade** error handling and logging

### **Intelligent News Fetching**
- **AI-Powered Query Understanding** - Natural language processing
- **Multi-Source Aggregation** - Google News + 9 RSS feeds
- **Smart Ranking** - AI ranks articles by relevance
- **Auto Image Extraction** - Fetches article images automatically
- **Location-Based Search** - Country/city-specific news

### **Performance**
- **Parallel Processing** - 2-3x faster searches
- **Caching System** - 30-minute TTL for repeated queries
- **Rate Limiting** - Prevents API abuse
- **Async Operations** - Non-blocking execution

### **Analytics**
- **System Metrics** - Success rates, response times
- **Agent Performance** - Individual agent statistics
- **Request Tracking** - Comprehensive logging

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                           │
│              (CLI / GUI / API Endpoints)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│               MULTI-AGENT ORCHESTRATOR                      │
│           (Coordinates & Routes Requests)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌────▼─────┐
│ QueryAgent   │  │GoogleNews   │  │RSSFeed   │
│ (AI Intent)  │  │Agent        │  │Agent     │
└──────────────┘  └─────────────┘  └──────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼──────┐  ┌──────▼──────┐  ┌────▼─────┐
│ RankingAgent │  │ContentAgent │  │Summary   │
│ (AI Ranking) │  │ (Extract)   │  │Agent     │
└──────────────┘  └─────────────┘  └──────────┘
```

### **Agent Responsibilities**

| Agent | Function | Technology |
|-------|----------|------------|
| **QueryAgent** | Parses user intent, extracts keywords, location, count | Google Gemini AI |
| **GoogleNewsAgent** | Fetches from Google News RSS + Image extraction | RSS + BeautifulSoup |
| **RSSFeedAgent** | Aggregates from 9 RSS sources + Image extraction | Feedparser |
| **ContentAgent** | Extracts full article text | Newspaper3k |
| **RankingAgent** | Ranks articles by relevance using AI | Google Gemini AI |
| **SummaryAgent** | Generates comprehensive AI summaries | Google Gemini AI |

---

## Quick Start

### **Prerequisites**
- Python 3.8 or higher
- Google AI Studio API Key (FREE)

### **1. Get Your FREE API Key**

1. Visit: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with Google account
3. Click **"Create API Key"**
4. Copy the key

> 💡 **Google AI Studio offers a generous FREE tier!**

### **2. Clone & Setup**

```bash
# Clone repository
git clone <your-repo-url>
cd News_Ai_Agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### **3. Configure API Key**

Create `backend/.env` file:

```env
GOOGLE_API_KEY=your_google_ai_studio_key_here
```

### **4. Run the Application**

#### **Option A: Command Line Interface (Recommended for testing)**

```bash
# From News_Ai_Agent directory
python run_cli.py
```

**Example queries:**
```
👤 You: Latest AI developments in India
👤 You: 10 technology news articles
👤 You: What's happening in Mumbai today?
👤 You: Give me 5 business news
```

#### **Option B: Web Interface (GUI)**

```bash
# From AI directory
python run_gui.py

# Open browser to: http://localhost:5000
```

---

## 📁 Project Structure

```
News_Ai_Agent/
├── backend/
│   ├── agents/                   # Specialized AI agents
│   │   ├── base_agent.py         # Base agent class
│   │   ├── query_agent.py        # Query understanding
│   │   ├── google_news_agent.py  # Google News fetcher
│   │   ├── rss_feed_agent.py     # RSS aggregator
│   │   ├── content_agent.py      # Content extractor
│   │   ├── ranking_agent.py      # AI ranking
│   │   └── summary_agent.py      # AI summarization
│   │
│   ├── services/
│   │   ├── orchestrator.py       # Multi-agent coordinator
│   │   ├── enhanced_fetch.py     # Enhanced fetcher service
│   │   └── production_agent.py   # Production-ready agent
│   │
│   ├── api/                      # REST API endpoints
│   │   └── routes.py
│   │
│   ├── config.py                  # Configuration
│   ├── server.py                  # Flask server
│   ├── main.py                    # CLI interface
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # API keys (create this)
│
├── frontend/                      # React web interface
│   ├── src/
│   ├── public/
│   └── package.json
│
├── run_cli.py                     # CLI launcher
├── run_gui.py                     # GUI launcher
└── README.md                      # This file
```

---

## Usage Examples

### **CLI Mode**

```bash
python run_cli.py
```

**Commands:**
- Type any news query naturally
- `more` - Show more articles from last query
- `stats` - View system and agent statistics
- `agents` - Check agent health status
- `parallel on/off` - Toggle parallel processing
- `help` - Show all commands
- `bye` - Exit

**Sample Queries:**

```
# Simple query (uses default 5 articles)
👤 You: AI news

# Specify article count
👤 You: 10 articles about climate change
👤 You: Give me 3 sports news
👤 You: Show 15 technology updates

# Location-based
👤 You: News from Mumbai
👤 You: What's happening in California?
👤 You: 5 articles about India today

# Category-based
👤 You: Latest business developments
👤 You: Cricket news today
👤 You: Space exploration updates
```

### **Web Interface**

```bash
python run_gui.py
```

1. Open browser to `http://localhost:5173`
2. Enter your query in the search box
3. Adjust settings:
   - Number of results
   - Enable/disable AI summaries
   - Parallel processing
4. View results with images, summaries, and sources

---

## 🔧 Configuration

### **Environment Variables** (`backend/.env`)

```env
# Required
GOOGLE_API_KEY=your_key_here

# Optional - Server config
FLASK_ENV=development
FLASK_PORT=5000
FLASK_DEBUG=True

# Optional - Cache config
CACHE_TTL_MINUTES=30

# Optional - Rate limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
```

### **System Settings** (`backend/config.py`)

```python
class Config:
    # API Keys
    GOOGLE_AI_STUDIO_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Caching
    CACHE_TTL_MINUTES = 30
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = 10  # per window
    RATE_LIMIT_WINDOW = 60    # seconds
    
    # Logging
    LOG_LEVEL = "INFO"
```

---

## API Endpoints

### **POST** `/api/news`

Fetch news articles

**Request:**
```json
{
  "query": "AI developments",
  "max_results": 10,
  "enrich": true,
  "parallel": true
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "title": "Article title",
      "description": "Brief description",
      "url": "https://...",
      "published": "2025-11-30",
      "source": "Source Name",
      "image": "https://...",
      "full_summary": "AI-generated summary...",
      "relevance_rank": 1,
      "agent": "GoogleNewsAgent"
    }
  ],
  "message": "Successfully fetched 10 articles",
  "metrics": {
    "response_time": "5.23s",
    "num_articles": 10,
    "parallel_processing": true
  }
}
```

### **GET** `/api/health`

Check system health

**Response:**
```json
{
  "status": "healthy",
  "agents": {
    "QueryAgent": "healthy",
    "GoogleNewsAgent": "healthy",
    "RSSFeedAgent": "healthy",
    "ContentAgent": "healthy",
    "RankingAgent": "healthy",
    "SummaryAgent": "healthy"
  }
}
```

### **GET** `/api/metrics`

Get system metrics

**Response:**
```json
{
  "total_requests": 42,
  "successful_requests": 40,
  "failed_requests": 2,
  "success_rate": "95.24%",
  "total_articles_delivered": 420
}
```

---

## Data Sources

### **Google News**
- Global news coverage
- Location-specific searches
- Real-time updates

### **RSS Feeds** (9 sources)
| Source | Categories |
|--------|------------|
| BBC World | General, Politics |
| BBC Technology | Tech |
| BBC Business | Business, Finance |
| BBC Science | Science, Environment |
| Reuters | World News |
| Al Jazeera | International |
| TechCrunch | Technology |
| The Verge | Tech, Science |
| Ars Technica | Technology |

> ✅ **All sources are FREE** - No API keys needed for news fetching

---

## Features in Detail

### **1. AI Query Understanding**

The **QueryAgent** uses Google Gemini to parse natural language:

```python
"10 tech articles from India" 
→ {
    keywords: ["tech", "technology"],
    location: "India",
    category: "technology",
    max_results: 10
  }
```

### **2. Parallel Search**

**GoogleNewsAgent** and **RSSFeedAgent** run simultaneously:

```
Sequential:  [Google 3s] → [RSS 4s] = 7s total
Parallel:    [Google 3s] ∥ [RSS 4s] = 4s total
```

### **3. Image Extraction**

Automatically extracts images from articles using:
- Open Graph meta tags (`og:image`)
- Twitter Card tags (`twitter:image`)
- Schema.org ImageObject
- First large image in article body

### **4. AI Ranking**

Articles ranked by relevance to query using:
- Title similarity
- Content relevance
- Source credibility
- Recency

### **5. AI Summaries**

Comprehensive 4-5 sentence summaries generated by Gemini AI:
- Covers key points
- Includes important details
- Professional news style
- Preserves context

---

## 📈 Performance

### **Response Times**

| Operation | Sequential | Parallel | Improvement |
|-----------|-----------|----------|-------------|
| Search | 7-10s | 4-6s | **2-3x faster** |
| With summaries | 15-20s | 10-12s | **40% faster** |
| Cached | <1s | <1s | **Instant** |

### **Resource Usage**

- **Memory**: ~200MB baseline, ~500MB with 10 enriched articles
- **CPU**: Moderate during AI operations
- **Network**: ~2-5MB per query (depending on images)

### **Rate Limits**

- **Google AI Studio**: 60 requests/minute (FREE tier)
- **RSS Feeds**: No limits (public)
- **Internal**: 10 requests/60 seconds (configurable)

---

## 🐛 Troubleshooting

### **Common Issues**

#### **1. "API Key Not Found"**
```bash
# Solution: Create .env file in backend/
echo "GOOGLE_API_KEY=your_key" > backend/.env
```

#### **2. "No articles found"**
- Check internet connection
- Try broader search terms
- Verify API key is active

#### **3. "Module not found"**
```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

#### **4. "Port 5000 already in use"**
```bash
# Solution: Change port in backend/config.py
FLASK_PORT = 5001
```

#### **5. Slow response times**
- Enable parallel processing: `parallel on`
- Reduce number of articles
- Check network connection

### **Logs**

Check logs for debugging:
```bash
# Logs are in backend/logs/
cat backend/logs/news_agent_*.log
```

---

## 🔒 Security

### **Best Practices**

1. **Never commit `.env` file**
   ```bash
   # Already in .gitignore
   backend/.env
   ```

2. **Use environment variables**
   ```python
   # ✅ Good
   api_key = os.getenv("GOOGLE_API_KEY")
   
   # ❌ Bad
   api_key = "hardcoded_key"
   ```

3. **Enable rate limiting**
   ```python
   RATE_LIMIT_REQUESTS = 10
   RATE_LIMIT_WINDOW = 60
   ```

4. **Validate inputs**
   - All user inputs are sanitized
   - Query length limited to 500 chars
   - Max results clamped to 1-50

---

## Deployment

### **Production Checklist**

- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use production WSGI server (Gunicorn)
- [ ] Enable HTTPS
- [ ] Set up monitoring/logging
- [ ] Configure firewall rules
- [ ] Set appropriate rate limits

---

## Testing

```bash
# Run tests
cd backend
python -m pytest tests/

# Test specific agent
python -m pytest tests/test_query_agent.py -v

# Test with coverage
python -m pytest --cov=agents tests/
```

---

## 📝 Development

### **Adding a New Agent**

1. Create agent in `backend/agents/`
2. Inherit from `BaseAgent`
3. Implement `process()` method
4. Register in `orchestrator.py`

```python
# Example: CustomAgent
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self, show_loading=True):
        super().__init__("CustomAgent", show_loading)
    
    def process(self, data, **kwargs):
        # Your logic here
        return processed_data
```

### **Adding a New RSS Source**

Edit `backend/agents/rss_feed_agent.py`:

```python
self.rss_sources = {
    # ... existing sources
    'new_source': 'https://newssite.com/rss.xml',
}

self.feed_mapping = {
    'technology': ['bbc_tech', 'new_source'],  # Add here
}
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - Free for personal and educational use

---

## 🙏 Acknowledgments

- **Google AI Studio** - For free AI model access
- **Newspaper3k** - Article extraction
- **Feedparser** - RSS parsing
- **BeautifulSoup** - HTML parsing
- **Flask** - Web framework

---

## 🎓 Educational Use

This project is perfect for learning:
- ✅ Multi-agent AI systems
- ✅ Parallel processing patterns
- ✅ Production-grade Python architecture
- ✅ RESTful API design
- ✅ AI model integration
- ✅ Web scraping techniques

**Kaggle Capstone Requirements:**
- ✅ **Multi-agent system**: 6 specialized agents
- ✅ **Tools**: Google AI, RSS parsers, content extractors
- ✅ **LLM Integration**: Google Gemini 2.5 Flash
- ✅ **Production Ready**: Caching, metrics, error handling

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/AbdullaVora/News_Ai_Agent?style=social)
![GitHub forks](https://img.shields.io/github/forks/AbdullaVora/News_Ai_Agent?style=social)
![GitHub issues](https://img.shields.io/github/issues/AbdullaVora/News_Ai_Agent)
![GitHub license](https://img.shields.io/github/license/AbdullaVora/News_Ai_Agent)

---

<div align="center">

**Built with ❤️ using Python & AI**

⭐ **Star this repo if you found it helpful!** ⭐

[Report Bug](https://github.com/AbdullaVora/News_Ai_Agent/issues) · [Request Feature](https://github.com/AbdullaVora/News_Ai_Agent/issues)

</div>