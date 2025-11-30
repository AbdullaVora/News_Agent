# """
# Google News Agent
# Specializes in fetching news from Google News RSS
# """

# import feedparser
# import requests
# import time
# from typing import List, Dict, Any, Optional
# from urllib.parse import quote_plus
# from bs4 import BeautifulSoup
# import sys
# import threading

# from base_agent import BaseAgent


# class LoadingSpinner:
#     """Terminal loading spinner"""
    
#     def __init__(self, message: str = "Loading"):
#         self.message = message
#         self.is_running = False
#         self.thread = None
#         self.spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
#         self.current = 0
    
#     def _spin(self):
#         while self.is_running:
#             sys.stdout.write(f'\r{self.spinners[self.current]} {self.message}...')
#             sys.stdout.flush()
#             self.current = (self.current + 1) % len(self.spinners)
#             time.sleep(0.1)
#         sys.stdout.write('\r' + ' ' * (len(self.message) + 5) + '\r')
#         sys.stdout.flush()
    
#     def start(self):
#         self.is_running = True
#         self.thread = threading.Thread(target=self._spin, daemon=True)
#         self.thread.start()
    
#     def stop(self):
#         self.is_running = False
#         if self.thread:
#             self.thread.join()


# class GoogleNewsAgent(BaseAgent):
#     """
#     Agent specialized in fetching from Google News
#     """
    
#     def __init__(self, show_loading: bool = True):
#         """Initialize Google News Agent"""
#         super().__init__("GoogleNewsAgent", show_loading)
#         self.base_url = "https://news.google.com/rss/search"
    
#     def process(self, data: Any, **kwargs) -> List[Dict]:
#         """
#         Fetch articles from Google News
        
#         Args:
#             data: Dict with 'search_term' and optional 'location'
#             kwargs: max_results (default 10)
            
#         Returns:
#             List of article dicts
#         """
#         # Health check
#         if kwargs.get('health_check'):
#             return []
        
#         if not isinstance(data, dict):
#             raise ValueError("Data must be a dict with 'search_term'")
        
#         search_term = data.get('search_term')
#         location = data.get('location')
#         max_results = kwargs.get('max_results', 10)
        
#         if not search_term:
#             raise ValueError("search_term is required")
        
#         # Show loading
#         spinner = None
#         if self.show_loading:
#             spinner = LoadingSpinner("🌐 Searching Google News")
#             spinner.start()
        
#         try:
#             articles = self._fetch_from_google(search_term, location, max_results)
            
#             if spinner:
#                 spinner.stop()
            
#             self.logger.info(f"Fetched {len(articles)} articles from Google News")
            
#             return articles
            
#         except Exception as e:
#             if spinner:
#                 spinner.stop()
#             raise e
    
#     def _fetch_from_google(
#         self, 
#         search_term: str, 
#         location: Optional[str], 
#         max_results: int
#     ) -> List[Dict]:
#         """Fetch articles from Google News RSS"""
        
#         articles = []
        
#         # Build URL
#         if location:
#             url = f"{self.base_url}?q={quote_plus(search_term)}+{quote_plus(location)}&hl=en-IN&gl=IN&ceid=IN:en"
#         else:
#             url = f"{self.base_url}?q={quote_plus(search_term)}&hl=en-IN&gl=IN&ceid=IN:en"
        
#         self.logger.debug(f"Fetching from: {url[:100]}...")
        
#         # Parse RSS feed
#         feed = feedparser.parse(url)
        
#         for entry in feed.entries[:max_results]:
#             try:
#                 # Clean title
#                 raw_title = entry.get('title', '')
#                 clean_title = BeautifulSoup(raw_title, 'html.parser').get_text()
                
#                 # Resolve Google redirect URL
#                 google_url = entry.get('link', '')
#                 actual_url = self._resolve_url(google_url)
                
#                 # Extract source
#                 source = 'Unknown'
#                 if ' - ' in clean_title:
#                     parts = clean_title.rsplit(' - ', 1)
#                     clean_title = parts[0].strip()
#                     source = parts[1].strip()
                
#                 if source == 'Unknown':
#                     source = entry.get('source', {}).get('title', 'Google News')
                
#                 article = {
#                     'title': clean_title,
#                     'description': BeautifulSoup(
#                         entry.get('summary', ''), 
#                         'html.parser'
#                     ).get_text(),
#                     'url': actual_url,
#                     'published': entry.get('published', ''),
#                     'source': source,
#                     'fetch_method': 'google_news',
#                     'agent': self.name
#                 }
                
#                 articles.append(article)
#                 time.sleep(0.3)  # Rate limiting
                
#             except Exception as e:
#                 self.logger.warning(f"Failed to parse entry: {e}")
#                 continue
        
#         return articles
    
#     def _resolve_url(self, google_url: str) -> str:
#         """Resolve Google News redirect URL to actual article URL"""
#         try:
#             response = requests.get(google_url, allow_redirects=True, timeout=5)
#             actual_url = response.url
            
#             # If still on Google domain, return original
#             if 'news.google.com' not in actual_url:
#                 return actual_url
            
#             return google_url
            
#         except Exception as e:
#             self.logger.debug(f"URL resolution failed: {e}")
#             return google_url

"""
Google News Agent
Specializes in fetching news from Google News RSS WITH image extraction
"""

import feedparser
import requests
import time
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
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


class GoogleNewsAgent(BaseAgent):
    """
    Agent specialized in fetching from Google News WITH IMAGE EXTRACTION
    """
    
    def __init__(self, show_loading: bool = True):
        """Initialize Google News Agent"""
        super().__init__("GoogleNewsAgent", show_loading)
        self.base_url = "https://news.google.com/rss/search"
    
    def process(self, data: Any, **kwargs) -> List[Dict]:
        """
        Fetch articles from Google News
        
        Args:
            data: Dict with 'search_term' and optional 'location'
            kwargs: max_results (default 10), extract_images (default True)
            
        Returns:
            List of article dicts with images
        """
        # Health check
        if kwargs.get('health_check'):
            return []
        
        if not isinstance(data, dict):
            raise ValueError("Data must be a dict with 'search_term'")
        
        search_term = data.get('search_term')
        location = data.get('location')
        max_results = kwargs.get('max_results', 10)
        extract_images = kwargs.get('extract_images', True)
        
        if not search_term:
            raise ValueError("search_term is required")
        
        # Show loading
        spinner = None
        if self.show_loading:
            spinner = LoadingSpinner("🌐 Searching Google News")
            spinner.start()
        
        try:
            articles = self._fetch_from_google(
                search_term, 
                location, 
                max_results,
                extract_images
            )
            
            if spinner:
                spinner.stop()
            
            self.logger.info(f"Fetched {len(articles)} articles from Google News")
            
            return articles
            
        except Exception as e:
            if spinner:
                spinner.stop()
            raise e
    
    def _fetch_from_google(
        self, 
        search_term: str, 
        location: Optional[str], 
        max_results: int,
        extract_images: bool = True
    ) -> List[Dict]:
        """Fetch articles from Google News RSS"""
        
        articles = []
        
        # Build URL
        if location:
            url = f"{self.base_url}?q={quote_plus(search_term)}+{quote_plus(location)}&hl=en-IN&gl=IN&ceid=IN:en"
        else:
            url = f"{self.base_url}?q={quote_plus(search_term)}&hl=en-IN&gl=IN&ceid=IN:en"
        
        self.logger.debug(f"Fetching from: {url[:100]}...")
        
        # Parse RSS feed
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:max_results]:
            try:
                # Clean title
                raw_title = entry.get('title', '')
                clean_title = BeautifulSoup(raw_title, 'html.parser').get_text()
                
                # Resolve Google redirect URL
                google_url = entry.get('link', '')
                actual_url = self._resolve_url(google_url)
                
                # Extract source
                source = 'Unknown'
                if ' - ' in clean_title:
                    parts = clean_title.rsplit(' - ', 1)
                    clean_title = parts[0].strip()
                    source = parts[1].strip()
                
                if source == 'Unknown':
                    source = entry.get('source', {}).get('title', 'Google News')
                
                article = {
                    'title': clean_title,
                    'description': BeautifulSoup(
                        entry.get('summary', ''), 
                        'html.parser'
                    ).get_text(),
                    'url': actual_url,
                    'published': entry.get('published', ''),
                    'source': source,
                    'image': None,  # Will be extracted if enabled
                    'fetch_method': 'google_news',
                    'agent': self.name
                }
                
                # Extract image from article page
                if extract_images:
                    article['image'] = self._extract_image(actual_url)
                
                articles.append(article)
                time.sleep(0.3)  # Rate limiting
                
            except Exception as e:
                self.logger.warning(f"Failed to parse entry: {e}")
                continue
        
        return articles
    
    def _resolve_url(self, google_url: str) -> str:
        """Resolve Google News redirect URL to actual article URL"""
        try:
            response = requests.get(google_url, allow_redirects=True, timeout=5)
            actual_url = response.url
            
            # If still on Google domain, return original
            if 'news.google.com' not in actual_url:
                return actual_url
            
            return google_url
            
        except Exception as e:
            self.logger.debug(f"URL resolution failed: {e}")
            return google_url
    
    def _extract_image(self, url: str) -> Optional[str]:
        """
        Extract image from article page
        Tries multiple methods:
        1. Open Graph meta tags
        2. Twitter Card meta tags
        3. First large image in article
        """
        try:
            # Set timeout to avoid hanging
            response = requests.get(
                url, 
                timeout=5,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Method 1: Try Open Graph image (most reliable)
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                image_url = og_image['content']
                self.logger.debug(f"✅ Found OG image: {image_url[:60]}...")
                return image_url
            
            # Method 2: Try Twitter Card image
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                image_url = twitter_image['content']
                self.logger.debug(f"✅ Found Twitter image: {image_url[:60]}...")
                return image_url
            
            # Method 3: Try schema.org ImageObject
            schema_image = soup.find('meta', attrs={'itemprop': 'image'})
            if schema_image and schema_image.get('content'):
                image_url = schema_image['content']
                self.logger.debug(f"✅ Found Schema image: {image_url[:60]}...")
                return image_url
            
            # Method 4: Find first large image in article body
            # Look for images in common article containers
            article_containers = soup.find_all(['article', 'main', 'div'], class_=lambda x: x and ('article' in x.lower() or 'content' in x.lower()))
            
            for container in article_containers:
                img = container.find('img', src=True)
                if img and img.get('src'):
                    # Filter out small icons/logos (usually < 200px)
                    width = img.get('width', '0')
                    if width and int(str(width).replace('px', '')) > 200:
                        image_url = img['src']
                        # Make absolute URL if relative
                        if image_url.startswith('//'):
                            image_url = 'https:' + image_url
                        elif image_url.startswith('/'):
                            from urllib.parse import urlparse
                            parsed = urlparse(url)
                            image_url = f"{parsed.scheme}://{parsed.netloc}{image_url}"
                        
                        self.logger.debug(f"✅ Found article image: {image_url[:60]}...")
                        return image_url
            
            self.logger.debug(f"⚠️ No image found for: {url[:60]}...")
            return None
            
        except requests.Timeout:
            self.logger.debug(f"⏱️ Timeout extracting image from: {url[:60]}...")
            return None
        except Exception as e:
            self.logger.debug(f"⚠️ Failed to extract image: {str(e)[:100]}")
            return None