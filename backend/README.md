# 🤖 Smart News Aggregator AI Agent

**Kaggle Capstone Project** - An intelligent news aggregator powered by Google AI Studio (FREE)

## ✨ Features

- 🔍 **Intelligent News Fetching** - No external paid APIs needed!
- 🧠 **AI-Powered Understanding** - Uses Google AI Studio to parse user intent
- 🌍 **Location-Based Search** - Fetch news from specific countries/cities
- 📊 **Smart Ranking** - AI ranks articles by relevance
- 🆓 **100% FREE** - Uses only free resources (Google AI Studio + RSS feeds)

---

## 🚀 Quick Start

### Step 1: Get Your FREE Google AI Studio API Key

1. Go to: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your key

**Note:** Google AI Studio offers FREE tier with generous limits!

### Step 2: Setup Project

```bash
# Clone or download the project
cd smart_news_ai

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run agent in GUI
python run_gui.py

# Run agent in terminal
python run_cli.py
```

### Step 3: Configure API Key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_ai_studio_key_here
```

### Step 4: Test News Fetching

```bash
python fetch_news.py
```
---

## 🎯 What Makes This Intelligent?

1. **AI Intent Parsing**: Your agent understands queries like:
   - "What's happening in Mumbai?"
   - "Latest tech news from Silicon Valley"
   - "Cricket news today"

2. **Multi-Source Fetching**: Pulls from:
   - Google News (location-specific)
   - BBC Feeds
   - Reuters
   - Al Jazeera
   - And more...

3. **Smart Ranking**: AI ranks articles by relevance to your query

---

## 📊 Meeting Kaggle Requirements

This project includes **3+ key concepts**:

✅ **Multi-agent system**: 
- Intent parser agent
- Fetch agent
- Ranking agent

✅ **Tools**:
- Google AI Studio (built-in LLM)
- Custom fetcher tool
- Web scraping tool

✅ **Agent powered by LLM**:
- Uses Google Gemini 1.5 Flash
- Intent parsing
- Content ranking

---

## Technical Architecture

```
User Query → AI Intent Parser → Multi-Source Fetcher → AI Ranker → Results
```

### Data Sources (All FREE):
- ✅ Google News
- ✅ BBC Feeds
- ✅ Reuters
- ✅ Al Jazeera
- ✅ More can be added easily

### NO API Keys Needed For:
- News fetching (RSS is open)
- Google News search
- Basic web scraping

### Only API Key Needed:
- Google AI Studio (FREE tier)

---

## 📁 Project Structure

```
smart_news_ai/
├── fetch_news.py          # Main fetcher (STEP 1 - COMPLETED ✓)
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env                   # API keys (create this)
├── README.md             # This file
│
├── clean_text.py         # STEP 2 (Next)
├── summarize.py          # STEP 3 (Next)
├── categorize.py         # STEP 4 (Next)
├── db.py                 # STEP 5 (Next)
├── agent.py              # STEP 6 (Next)
└── main.py               # STEP 7 (Next)
```

## 💡 Example Queries You Can Try

```python
# Location-based
"News from Mumbai"
"What's happening in California today"
"Latest updates from UK"

# Category-based
"AI and machine learning news"
"Cricket scores"
"Stock market updates"
"Climate change articles"

# Time-based
"Today's headlines"
"Latest breaking news"
"Recent developments in space exploration"

# Mixed
"Technology news from India today"
"Sports news from Europe"
"Healthcare updates from WHO"
```

---

## 🌟 Key Advantages

1. **No Paid APIs**: Everything uses free resources
2. **Intelligent**: AI understands natural language queries
3. **Scalable**: Easy to add more sources
4. **Kaggle-Ready**: Meets all submission requirements
5. **Real-World Ready**: Can be deployed anywhere

---

## 📝 Notes

- Google AI Studio FREE tier: 60 requests per minute
- RSS feeds are public and free to use
- Be respectful with request rates
- Works in Kaggle notebooks!

---

## 🤝 Support

**Need help?**
- Check Google AI Studio docs: [ai.google.dev](https://ai.google.dev)
- RSS feed issues: Make sure your internet connection is stable
- API errors: Verify your API key is active

---

## 📄 License

MIT License - Free for personal and educational use

---
