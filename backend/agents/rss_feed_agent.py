"""
RSS Feed Agent
Specializes in fetching news from various RSS feeds
"""

import feedparser
import time
import sys
import threading
from typing import List, Dict, Any

from base_agent import BaseAgent


class LoadingSpinner:
    """Terminal loading spinner"""
    
    def __init__(self, message: str = "Loading"):
        self.message = message
        self.is_running = False
        self.thread = None
        self.spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current = 0
    
    def _spin(self):
        while self.is_running:
            sys.stdout.write(f'\r{self.spinners[self.current]} {self.message}...')
            sys.stdout.flush()
            self.current = (self.current + 1) % len(self.spinners)
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 5) + '\r')
        sys.stdout.flush()
    
    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()


class RSSFeedAgent(BaseAgent):
    """
    Agent specialized in fetching from RSS feeds
    """
    
    def __init__(self, show_loading: bool = True):
        """Initialize RSS Feed Agent"""
        super().__init__("RSSFeedAgent", show_loading)
        
        # RSS Feed sources
        self.rss_sources = {
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
        
        # Category to feed mapping
        self.feed_mapping = {
            'technology': ['bbc_tech', 'techcrunch', 'the_verge', 'ars_technica'],
            'business': ['bbc_business', 'reuters_world'],
            'science': ['bbc_science'],
            'sports': ['bbc_world'],
            'politics': ['bbc_world', 'al_jazeera'],
            'general': ['bbc_world', 'al_jazeera', 'reuters_world'],
        }
    
    def process(self, data: Any, **kwargs) -> List[Dict]:
        """
        Fetch articles from RSS feeds
        
        Args:
            data: Dict with 'category' and 'keywords'
            kwargs: max_results_per_feed (default 8)
            
        Returns:
            List of article dicts
        """
        # Health check
        if kwargs.get('health_check'):
            return []
        
        if not isinstance(data, dict):
            raise ValueError("Data must be a dict with 'category'")
        
        category = data.get('category', 'general')
        max_per_feed = kwargs.get('max_results_per_feed', 8)
        
        # Show loading
        spinner = None
        if self.show_loading:
            spinner = LoadingSpinner("📡 Gathering from RSS feeds")
            spinner.start()
        
        try:
            articles = self._fetch_from_feeds(category, max_per_feed)
            
            if spinner:
                spinner.stop()
            
            self.logger.info(f"Fetched {len(articles)} articles from RSS feeds")
            
            return articles
            
        except Exception as e:
            if spinner:
                spinner.stop()
            raise e
    
    def _fetch_from_feeds(self, category: str, max_per_feed: int) -> List[Dict]:
        """Fetch articles from relevant RSS feeds"""
        
        articles = []
        
        # Get relevant feeds for category
        feeds_to_check = self.feed_mapping.get(category, ['bbc_world', 'al_jazeera'])
        
        # Always include general news feeds
        if category != 'general':
            feeds_to_check.extend(['bbc_world', 'al_jazeera'])
        
        # Remove duplicates
        feeds_to_check = list(set(feeds_to_check))
        
        self.logger.debug(f"Checking {len(feeds_to_check)} feeds for category: {category}")
        
        for feed_name in feeds_to_check:
            if feed_name not in self.rss_sources:
                continue
            
            try:
                feed_articles = self._parse_feed(feed_name, max_per_feed)
                articles.extend(feed_articles)
                
                time.sleep(0.5)  # Rate limiting between feeds
                
            except Exception as e:
                self.logger.warning(f"Failed to fetch from {feed_name}: {e}")
                continue
        
        return articles
    
    def _parse_feed(self, feed_name: str, max_results: int) -> List[Dict]:
        """Parse a single RSS feed"""
        
        feed_url = self.rss_sources[feed_name]
        
        self.logger.debug(f"Parsing feed: {feed_name}")
        
        feed = feedparser.parse(feed_url)
        
        articles = []
        
        for entry in feed.entries[:max_results]:
            try:
                article = {
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', entry.get('description', '')),
                    'url': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'source': feed_name.replace('_', ' ').title(),
                    'fetch_method': 'rss_direct',
                    'agent': self.name
                }
                
                articles.append(article)
                
            except Exception as e:
                self.logger.warning(f"Failed to parse entry in {feed_name}: {e}")
                continue
        
        return articles