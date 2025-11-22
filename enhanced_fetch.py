"""
Enhanced Smart News Aggregator - Full URLs, Full Summaries
Fetches complete article content and generates comprehensive summaries
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Dict
import google.generativeai as genai
from urllib.parse import quote_plus, urlparse
import re
from newspaper import Article  # For full article extraction

class EnhancedNewsFetcher:
    """
    Enhanced fetcher with full URL resolution and comprehensive summaries
    """
    
    def __init__(self, google_ai_studio_key: str):
        """Initialize with Google AI Studio API key"""
        genai.configure(api_key=google_ai_studio_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Expanded FREE RSS sources
        self.rss_sources = {
            'google_news': 'https://news.google.com/rss',
            'bbc_world': 'http://feeds.bbci.co.uk/news/world/rss.xml',
            'bbc_tech': 'http://feeds.bbci.co.uk/news/technology/rss.xml',
            'bbc_business': 'http://feeds.bbci.co.uk/news/business/rss.xml',
            'bbc_science': 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
            'reuters_world': 'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
            'al_jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
            'techcrunch': 'https://techcrunch.com/feed/',
            'the_verge': 'https://www.theverge.com/rss/index.xml',
            'ars_technica': 'https://feeds.arstechnica.com/arstechnica/index',
        }
        
    def resolve_google_news_url(self, google_url: str) -> str:
        """
        Resolve Google News redirect URL to actual article URL
        """
        try:
            # Google News URLs contain the actual URL in the path
            # Format: https://news.google.com/rss/articles/[encoded_url]
            
            # Try to follow redirect
            response = requests.get(google_url, allow_redirects=True, timeout=5)
            actual_url = response.url
            
            # Clean up URL
            if 'news.google.com' not in actual_url:
                return actual_url
            
            return google_url  # Return original if resolution fails
            
        except Exception as e:
            print(f"⚠ URL resolution failed: {e}")
            return google_url
    
    def extract_full_article(self, url: str) -> Dict[str, str]:
        """
        Extract full article content using newspaper3k
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'full_text': article.text,
                'authors': article.authors,
                'publish_date': str(article.publish_date) if article.publish_date else '',
                'top_image': article.top_image,
            }
        except Exception as e:
            print(f"⚠ Article extraction failed for {url[:50]}: {e}")
            return {'full_text': '', 'authors': [], 'publish_date': '', 'top_image': ''}
    
    def generate_comprehensive_summary(self, article_text: str, title: str) -> str:
        """
        Generate a comprehensive summary using AI
        """
        if not article_text or len(article_text) < 100:
            return "Summary not available - could not extract article content."
        
        prompt = f"""
        Generate a comprehensive 4-5 sentence summary of this news article:
        
        Title: {title}
        
        Article:
        {article_text[:3000]}  # Limit to save tokens
        
        Summary should:
        - Cover all key points
        - Be clear and informative
        - Include important details, names, and numbers
        - Be written in a professional news style
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"⚠ AI summary failed: {e}")
            # Fallback: return first 3 sentences
            sentences = article_text.split('. ')[:3]
            return '. '.join(sentences) + '.'
    
    def parse_user_query(self, user_query: str) -> Dict:
        """Parse user intent with AI"""
        prompt = f"""
        Analyze this news search query and extract structured information:
        Query: "{user_query}"
        
        Return ONLY a JSON object with these fields:
        {{
            "keywords": ["list", "of", "keywords"],
            "location": "country/state/city or null",
            "category": "technology/sports/politics/business/health/entertainment or general",
            "timeframe": "latest/today/recent or null",
            "search_term": "optimized search term for news search"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            result_text = re.sub(r'```json\s*|\s*```', '', result_text)
            
            import json
            parsed_intent = json.loads(result_text)
            print(f"✓ Parsed intent: {parsed_intent}")
            return parsed_intent
            
        except Exception as e:
            print(f"⚠ AI parsing failed: {e}")
            return {
                "keywords": user_query.split(),
                "location": None,
                "category": "general",
                "search_term": user_query
            }
    
    def fetch_google_news_rss(self, search_term: str, location: str = None) -> List[Dict]:
        """Fetch from Google News with full URL resolution"""
        articles = []
        
        try:
            if location:
                base_url = f"https://news.google.com/rss/search?q={quote_plus(search_term)}+{quote_plus(location)}&hl=en-IN&gl=IN&ceid=IN:en"
            else:
                base_url = f"https://news.google.com/rss/search?q={quote_plus(search_term)}&hl=en-IN&gl=IN&ceid=IN:en"
            
            print(f"🔍 Fetching from Google News...")
            feed = feedparser.parse(base_url)
            
            for entry in feed.entries[:10]:
                # Resolve actual URL
                google_url = entry.get('link', '')
                actual_url = self.resolve_google_news_url(google_url)
                
                article = {
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', ''),
                    'url': actual_url,
                    'published': entry.get('published', ''),
                    'source': entry.get('source', {}).get('title', 'Unknown'),
                    'fetch_method': 'google_news'
                }
                articles.append(article)
                
                time.sleep(0.3)  # Rate limiting
            
            print(f"✓ Fetched {len(articles)} from Google News")
            
        except Exception as e:
            print(f"⚠ Google News error: {e}")
        
        return articles
    
    def fetch_all_rss_feeds(self, category: str, keywords: List[str]) -> List[Dict]:
        """
        Fetch from ALL RSS sources, not just a few
        """
        articles = []
        
        # Map categories to relevant feeds
        feed_mapping = {
            'technology': ['bbc_tech', 'techcrunch', 'the_verge', 'ars_technica'],
            'business': ['bbc_business', 'reuters_world'],
            'science': ['bbc_science'],
            'general': ['bbc_world', 'al_jazeera', 'reuters_world'],
            'world': ['bbc_world', 'al_jazeera', 'reuters_world'],
        }
        
        # Get relevant feeds for category
        feeds_to_check = feed_mapping.get(category, ['bbc_world', 'al_jazeera'])
        
        # Also add some general feeds
        if category != 'general':
            feeds_to_check.extend(['bbc_world', 'al_jazeera'])
        
        # Remove duplicates
        feeds_to_check = list(set(feeds_to_check))
        
        print(f"🔍 Checking {len(feeds_to_check)} RSS feeds: {feeds_to_check}")
        
        for feed_name in feeds_to_check:
            if feed_name not in self.rss_sources:
                continue
                
            try:
                feed_url = self.rss_sources[feed_name]
                print(f"  📡 Fetching {feed_name}...")
                
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:8]:  # Get 8 from each
                    article = {
                        'title': entry.get('title', ''),
                        'description': entry.get('summary', entry.get('description', '')),
                        'url': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'source': feed_name.replace('_', ' ').title(),
                        'fetch_method': 'rss_direct'
                    }
                    articles.append(article)
                
                time.sleep(0.5)  # Be respectful
                
            except Exception as e:
                print(f"  ⚠ {feed_name} error: {e}")
        
        print(f"✓ Fetched {len(articles)} from RSS feeds")
        return articles
    
    def enrich_articles(self, articles: List[Dict], max_to_enrich: int = 10) -> List[Dict]:
        """
        Extract full content and generate summaries for top articles
        """
        print(f"\n📝 Enriching top {max_to_enrich} articles with full content...")
        
        enriched = []
        
        for i, article in enumerate(articles[:max_to_enrich]):
            print(f"  Processing {i+1}/{max_to_enrich}: {article['title'][:50]}...")
            
            try:
                # Extract full article
                full_content = self.extract_full_article(article['url'])
                
                # Generate comprehensive summary
                if full_content['full_text']:
                    summary = self.generate_comprehensive_summary(
                        full_content['full_text'],
                        article['title']
                    )
                else:
                    summary = article['description']
                
                # Update article
                article['full_summary'] = summary
                article['full_text'] = full_content['full_text'][:500]  # Preview
                article['authors'] = full_content['authors']
                
                enriched.append(article)
                
                time.sleep(1)  # Rate limiting for AI
                
            except Exception as e:
                print(f"  ⚠ Enrichment failed: {e}")
                article['full_summary'] = article['description']
                enriched.append(article)
        
        print(f"✓ Enriched {len(enriched)} articles")
        return enriched
    
    def rank_articles_with_ai(self, articles: List[Dict], user_query: str) -> List[Dict]:
        """Rank articles by relevance"""
        if not articles:
            return []
        
        article_summaries = []
        for i, art in enumerate(articles[:30]):
            article_summaries.append(
                f"{i+1}. {art['title']} - {art['description'][:100]}"
            )
        
        prompt = f"""
        User query: "{user_query}"
        
        Rank these articles by relevance (most to least relevant).
        Return ONLY a JSON array of article numbers: [5, 2, 8, 1, ...]
        Include top 15 most relevant articles.
        
        Articles:
        {chr(10).join(article_summaries)}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            result_text = re.sub(r'```json\s*|\s*```', '', result_text)
            
            import json
            ranked_indices = json.loads(result_text)
            
            ranked_articles = []
            for idx in ranked_indices:
                if 0 < idx <= len(articles):
                    ranked_articles.append(articles[idx-1])
            
            print(f"✓ AI ranked {len(ranked_articles)} articles")
            return ranked_articles
            
        except Exception as e:
            print(f"⚠ Ranking failed: {e}")
            return articles
    
    def fetch_news(self, user_query: str, max_results: int = 10, enrich: bool = True) -> List[Dict]:
        """
        Main method: Comprehensive news fetching with full content
        """
        print(f"\n{'='*70}")
        print(f"🤖 ENHANCED NEWS FETCH: '{user_query}'")
        print(f"{'='*70}\n")
        
        # Parse intent
        intent = self.parse_user_query(user_query)
        
        # Fetch from Google News
        google_articles = self.fetch_google_news_rss(
            search_term=intent['search_term'],
            location=intent.get('location')
        )
        
        # Fetch from ALL other RSS sources
        rss_articles = self.fetch_all_rss_feeds(
            category=intent['category'],
            keywords=intent['keywords']
        )
        
        # Combine all articles
        all_articles = google_articles + rss_articles
        
        print(f"\n📊 Total articles collected: {len(all_articles)}")
        
        # Rank by relevance
        ranked_articles = self.rank_articles_with_ai(all_articles, user_query)
        
        # Enrich top articles with full content
        if enrich:
            final_results = self.enrich_articles(ranked_articles[:max_results])
        else:
            final_results = ranked_articles[:max_results]
        
        print(f"\n{'='*70}")
        print(f"✅ RETURNING {len(final_results)} ENRICHED ARTICLES")
        print(f"{'='*70}\n")
        
        return final_results


# ============================================
# EXAMPLE USAGE
# ============================================

if __name__ == "__main__":
    from config import Config
    
    # Initialize enhanced fetcher
    fetcher = EnhancedNewsFetcher(Config.GOOGLE_AI_STUDIO_KEY)
    
    # Test query
    results = fetcher.fetch_news("AI developments in India", max_results=5)
    
    # Display results with full details
    print("\n" + "="*70)
    print("📰 ENHANCED RESULTS WITH FULL SUMMARIES")
    print("="*70 + "\n")
    
    for i, article in enumerate(results, 1):
        print(f"\n{'─'*70}")
        print(f"Article {i}: {article['title']}")
        print(f"{'─'*70}")
        print(f"📍 Source: {article['source']}")
        print(f"🔗 URL: {article['url']}")
        print(f"📅 Published: {article['published']}")
        if article.get('authors'):
            print(f"✍️  Authors: {', '.join(article['authors'])}")
        print(f"\n📝 Summary:")
        print(article.get('full_summary', article['description']))
        print()