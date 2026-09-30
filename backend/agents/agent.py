"""
Production-Ready Smart News Agent
Enterprise-grade news aggregation with caching, monitoring, and error handling
"""

import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from functools import wraps
import time
import hashlib
import json
from pathlib import Path
import traceback

from services.enhanced_fetch import EnhancedNewsFetcher
from config import Config


# ============================================
# LOGGING CONFIGURATION
# ============================================

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Configure production logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("NewsAgent")
    logger.setLevel(getattr(logging, log_level))
    
    # File handler with rotation
    file_handler = logging.FileHandler(
        log_dir / f"news_agent_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# ============================================
# SIMPLE IN-MEMORY CACHE
# ============================================

class SimpleCache:
    """In-memory cache with TTL"""
    
    def __init__(self, ttl_minutes: int = 30):
        self.cache: Dict[str, Tuple[datetime, any]] = {}
        self.ttl = timedelta(minutes=ttl_minutes)
        self.logger = logging.getLogger("NewsAgent.Cache")
    
    def _generate_key(self, query: str, max_results: int) -> str:
        """Generate cache key"""
        data = f"{query}:{max_results}".encode()
        return hashlib.md5(data).hexdigest()
    
    def get(self, query: str, max_results: int) -> Optional[List[Dict]]:
        """Get cached results"""
        key = self._generate_key(query, max_results)
        
        if key in self.cache:
            timestamp, data = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                self.logger.info(f"Cache HIT for query: {query[:50]}")
                return data
            else:
                # Expired
                del self.cache[key]
                self.logger.debug(f"Cache EXPIRED for query: {query[:50]}")
        
        self.logger.info(f"Cache MISS for query: {query[:50]}")
        return None
    
    def set(self, query: str, max_results: int, data: List[Dict]):
        """Cache results"""
        key = self._generate_key(query, max_results)
        self.cache[key] = (datetime.now(), data)
        self.logger.debug(f"Cached results for: {query[:50]}")
    
    def clear(self):
        """Clear entire cache"""
        self.cache.clear()
        self.logger.info("Cache cleared")
    
    def clear_expired(self):
        """Remove expired entries"""
        now = datetime.now()
        expired_keys = [
            k for k, (ts, _) in self.cache.items()
            if now - ts >= self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self.logger.info(f"Cleared {len(expired_keys)} expired cache entries")


# ============================================
# METRICS COLLECTOR
# ============================================

class MetricsCollector:
    """Collect and track agent metrics"""
    
    def __init__(self):
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_articles_fetched': 0,
            'avg_response_time': 0.0,
            'response_times': [],
        }
        self.logger = logging.getLogger("NewsAgent.Metrics")
    
    def record_request(self, success: bool, response_time: float, num_articles: int, from_cache: bool):
        """Record request metrics"""
        self.metrics['total_requests'] += 1
        
        if success:
            self.metrics['successful_requests'] += 1
            self.metrics['total_articles_fetched'] += num_articles
        else:
            self.metrics['failed_requests'] += 1
        
        if from_cache:
            self.metrics['cache_hits'] += 1
        else:
            self.metrics['cache_misses'] += 1
        
        self.metrics['response_times'].append(response_time)
        self.metrics['avg_response_time'] = sum(self.metrics['response_times']) / len(self.metrics['response_times'])
    
    def get_summary(self) -> Dict:
        """Get metrics summary"""
        total = self.metrics['total_requests']
        return {
            'total_requests': total,
            'success_rate': f"{(self.metrics['successful_requests'] / total * 100) if total > 0 else 0:.2f}%",
            'cache_hit_rate': f"{(self.metrics['cache_hits'] / total * 100) if total > 0 else 0:.2f}%",
            'avg_articles_per_request': f"{self.metrics['total_articles_fetched'] / total if total > 0 else 0:.2f}",
            'avg_response_time': f"{self.metrics['avg_response_time']:.2f}s",
            'total_articles_delivered': self.metrics['total_articles_fetched'],
        }
    
    def print_summary(self):
        """Print metrics summary"""
        summary = self.get_summary()
        self.logger.info("=== AGENT METRICS SUMMARY ===")
        for key, value in summary.items():
            self.logger.info(f"  {key}: {value}")


# ============================================
# RATE LIMITER
# ============================================

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window  # seconds
        self.requests: List[float] = []
        self.logger = logging.getLogger("NewsAgent.RateLimiter")
    
    def is_allowed(self) -> bool:
        """Check if request is allowed"""
        now = time.time()
        
        # Remove old requests outside time window
        self.requests = [ts for ts in self.requests if now - ts < self.time_window]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        
        self.logger.warning("Rate limit exceeded")
        return False
    
    def wait_time(self) -> float:
        """Get seconds to wait before next request"""
        if not self.requests:
            return 0.0
        
        oldest = min(self.requests)
        wait = self.time_window - (time.time() - oldest)
        return max(0.0, wait)


# ============================================
# DECORATORS
# ============================================

def retry_on_failure(max_retries: int = 3, delay: float = 2.0):
    """Retry decorator for failed operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger("NewsAgent")
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_retries} attempts failed: {e}")
                        raise
            
        return wrapper
    return decorator


def measure_time(func):
    """Measure execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        
        logger = logging.getLogger("NewsAgent")
        logger.debug(f"{func.__name__} took {elapsed:.2f}s")
        
        return result, elapsed
    
    return wrapper


# ============================================
# PRODUCTION NEWS AGENT
# ============================================

class ProductionNewsAgent:
    """
    Production-ready news agent with caching, metrics, and error handling
    """
    
    def __init__(
        self,
        api_key: str,
        cache_ttl_minutes: int = 30,
        rate_limit_requests: int = 10,
        rate_limit_window: int = 60,
        log_level: str = "INFO"
    ):
        """Initialize production agent"""
        
        # Setup logging
        self.logger = setup_logging(log_level)
        self.logger.info("Initializing ProductionNewsAgent...")
        
        # Validate config
        try:
            Config.validate()
            self.logger.info("Configuration validated successfully")
        except Exception as e:
            self.logger.critical(f"Configuration validation failed: {e}")
            raise
        
        # Initialize components
        try:
            self.fetcher = EnhancedNewsFetcher(api_key)
            self.cache = SimpleCache(ttl_minutes=cache_ttl_minutes)
            self.metrics = MetricsCollector()
            self.rate_limiter = RateLimiter(
                max_requests=rate_limit_requests,
                time_window=rate_limit_window
            )
            
            self.logger.info("All components initialized successfully")
            self.logger.info(f"Cache TTL: {cache_ttl_minutes} minutes")
            self.logger.info(f"Rate limit: {rate_limit_requests} requests per {rate_limit_window}s")
            
        except Exception as e:
            self.logger.critical(f"Failed to initialize components: {e}")
            raise
    
    @retry_on_failure(max_retries=2, delay=3.0)
    def fetch_news(
        self,
        query: str,
        max_results: int = 10,
        enrich: bool = True,
        use_cache: bool = True,
        force_refresh: bool = False
    ) -> Dict:
        """
        Fetch news with production features
        
        Returns:
            Dict with keys: success, data, message, metrics, from_cache
        """
        
        start_time = time.time()
        
        # Input validation
        if not query or not query.strip():
            self.logger.error("Empty query received")
            return {
                'success': False,
                'data': [],
                'message': 'Query cannot be empty',
                'metrics': None,
                'from_cache': False
            }
        
        if max_results < 1 or max_results > 50:
            self.logger.warning(f"Invalid max_results: {max_results}, clamping to 1-50")
            max_results = max(1, min(50, max_results))
        
        query = query.strip()
        
        self.logger.info(f"Processing query: '{query[:100]}' (max_results={max_results}, enrich={enrich})")
        
        # Check rate limit
        if not self.rate_limiter.is_allowed():
            wait_time = self.rate_limiter.wait_time()
            self.logger.warning(f"Rate limit exceeded. Wait {wait_time:.1f}s")
            return {
                'success': False,
                'data': [],
                'message': f'Rate limit exceeded. Please wait {wait_time:.1f} seconds.',
                'metrics': None,
                'from_cache': False
            }
        
        # Check cache
        from_cache = False
        if use_cache and not force_refresh:
            cached_results = self.cache.get(query, max_results)
            if cached_results:
                elapsed = time.time() - start_time
                self.metrics.record_request(True, elapsed, len(cached_results), True)
                
                self.logger.info(f"Returning {len(cached_results)} cached results")
                
                return {
                    'success': True,
                    'data': cached_results,
                    'message': 'Results from cache',
                    'metrics': {
                        'response_time': f"{elapsed:.2f}s",
                        'num_articles': len(cached_results),
                        'from_cache': True
                    },
                    'from_cache': True
                }
        
        # Fetch fresh results
        try:
            self.logger.info("Fetching fresh results...")
            results = self.fetcher.fetch_news(query, max_results=max_results, enrich=enrich)
            
            elapsed = time.time() - start_time
            
            if results:
                # Cache results
                if use_cache:
                    self.cache.set(query, max_results, results)
                
                self.metrics.record_request(True, elapsed, len(results), False)
                
                self.logger.info(f"Successfully fetched {len(results)} articles in {elapsed:.2f}s")
                
                return {
                    'success': True,
                    'data': results,
                    'message': f'Successfully fetched {len(results)} articles',
                    'metrics': {
                        'response_time': f"{elapsed:.2f}s",
                        'num_articles': len(results),
                        'from_cache': False
                    },
                    'from_cache': False
                }
            else:
                self.logger.warning("No results found")
                self.metrics.record_request(False, elapsed, 0, False)
                
                return {
                    'success': False,
                    'data': [],
                    'message': 'No articles found for the given query',
                    'metrics': {
                        'response_time': f"{elapsed:.2f}s",
                        'num_articles': 0,
                        'from_cache': False
                    },
                    'from_cache': False
                }
        
        except Exception as e:
            elapsed = time.time() - start_time
            self.metrics.record_request(False, elapsed, 0, False)
            
            self.logger.error(f"Error fetching news: {e}")
            self.logger.debug(traceback.format_exc())
            
            return {
                'success': False,
                'data': [],
                'message': f'Error: {str(e)}',
                'metrics': {
                    'response_time': f"{elapsed:.2f}s",
                    'num_articles': 0,
                    'from_cache': False
                },
                'from_cache': False
            }
    
    def get_metrics(self) -> Dict:
        """Get agent metrics"""
        return self.metrics.get_summary()
    
    def print_metrics(self):
        """Print metrics to log"""
        self.metrics.print_summary()
    
    def clear_cache(self):
        """Clear cache"""
        self.cache.clear()
        self.logger.info("Cache cleared by user request")
    
    def health_check(self) -> Dict:
        """Check agent health"""
        try:
            # Test AI model
            test_response = self.fetcher.model.generate_content("Say 'OK'")
            ai_healthy = "ok" in test_response.text.lower()
        except:
            ai_healthy = False
        
        return {
            'status': 'healthy' if ai_healthy else 'degraded',
            'ai_model': 'operational' if ai_healthy else 'unavailable',
            'cache': 'operational',
            'metrics': self.get_metrics()
        }


# ============================================
# PRODUCTION USAGE EXAMPLE
# ============================================

def main():
    """Production usage example"""
    
    # Initialize agent
    agent = ProductionNewsAgent(
        api_key=Config.GOOGLE_AI_STUDIO_KEY,
        cache_ttl_minutes=30,
        rate_limit_requests=10,
        rate_limit_window=60,
        log_level="INFO"
    )
    
    # Health check
    health = agent.health_check()
    print(f"\n🏥 Health Check: {health['status'].upper()}")
    print(f"   AI Model: {health['ai_model']}")
    
    # Sample queries
    queries = [
        "AI developments in India",
        "cybersecurity news today",
        "latest technology trends"
    ]
    
    print("\n" + "="*80)
    print("🚀 PRODUCTION AGENT DEMO")
    print("="*80)
    
    for query in queries:
        print(f"\n📰 Query: {query}")
        print("-" * 80)
        
        # Fetch news
        response = agent.fetch_news(query, max_results=5, enrich=True)
        
        if response['success']:
            print(f"✅ {response['message']}")
            print(f"⏱️  Response time: {response['metrics']['response_time']}")
            print(f"📊 From cache: {response['from_cache']}")
            print(f"\nTop 3 articles:")
            
            for i, article in enumerate(response['data'][:3], 1):
                print(f"  {i}. {article['title'][:80]}")
                print(f"     Source: {article['source']} | {article['published']}")
        else:
            print(f"❌ {response['message']}")
        
        time.sleep(2)  # Simulate delay between requests
    
    # Print metrics
    print("\n" + "="*80)
    print("📊 AGENT METRICS")
    print("="*80)
    agent.print_metrics()
    
    print("\n✅ Production demo completed!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        traceback.print_exc()