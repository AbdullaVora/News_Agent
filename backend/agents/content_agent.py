"""
Content Extraction Agent
Specializes in extracting full article content
"""

import time
from typing import List, Dict, Any
from newspaper import Article
import sys
import threading

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


class ContentAgent(BaseAgent):
    """
    Agent specialized in extracting full article content
    """
    
    def __init__(self, show_loading: bool = True):
        """Initialize Content Agent"""
        super().__init__("ContentAgent", show_loading)
    
    def process(self, data: Any, **kwargs) -> List[Dict]:
        """
        Extract full content from articles
        
        Args:
            data: List of article dicts with 'url'
            kwargs: max_to_extract (default 10)
            
        Returns:
            List of enriched article dicts
        """
        # Health check
        if kwargs.get('health_check'):
            return []
        
        if not isinstance(data, list):
            raise ValueError("Data must be a list of article dicts")
        
        max_to_extract = kwargs.get('max_to_extract', 10)
        
        # Show loading
        spinner = None
        if self.show_loading:
            spinner = LoadingSpinner("📄 Extracting article content")
            spinner.start()
        
        try:
            enriched_articles = self._extract_content(data[:max_to_extract])
            
            if spinner:
                spinner.stop()
            
            self.logger.info(f"Extracted content from {len(enriched_articles)} articles")
            
            return enriched_articles
            
        except Exception as e:
            if spinner:
                spinner.stop()
            raise e
    
    def _extract_content(self, articles: List[Dict]) -> List[Dict]:
        """Extract full content from articles"""
        
        enriched = []
        
        for i, article in enumerate(articles, 1):
            try:
                url = article.get('url')
                
                if not url:
                    self.logger.warning(f"Article {i} has no URL, skipping")
                    enriched.append(article)
                    continue
                
                # Extract content
                full_content = self._extract_from_url(url)
                
                # Add to article
                article['full_text'] = full_content['full_text'][:500]  # First 500 chars
                article['authors'] = full_content['authors']
                article['publish_date'] = full_content['publish_date']
                article['top_image'] = full_content['top_image']
                article['has_full_content'] = bool(full_content['full_text'])
                
                enriched.append(article)
                
                # Small delay between requests
                time.sleep(0.5)
                
            except Exception as e:
                self.logger.warning(f"Failed to extract content from article {i}: {e}")
                article['has_full_content'] = False
                enriched.append(article)
        
        return enriched
    
    def _extract_from_url(self, url: str) -> Dict[str, Any]:
        """Extract content from a single URL"""
        
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
            self.logger.debug(f"Content extraction failed for {url[:50]}: {e}")
            
            return {
                'full_text': '',
                'authors': [],
                'publish_date': '',
                'top_image': ''
            }