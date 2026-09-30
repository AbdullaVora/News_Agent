"""
Ranking Agent
Specializes in ranking articles by relevance
"""

import json
import re
import sys
import time
import threading
from typing import List, Dict, Any
import google.generativeai as genai

from .base_agent import BaseAgent


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


class RankingAgent(BaseAgent):
    """
    Agent specialized in ranking articles by relevance using AI
    """
    
    def __init__(self, api_key: str, show_loading: bool = True):
        """Initialize Ranking Agent"""
        super().__init__("RankingAgent", show_loading)
        
        # Configure AI model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        self.logger.info("AI model configured for ranking")
    
    def process(self, data: Any, **kwargs) -> List[Dict]:
        """
        Rank articles by relevance to query
        
        Args:
            data: Dict with 'articles' (list) and 'query' (str)
            kwargs: top_n (default 15)
            
        Returns:
            List of ranked articles
        """
        # Health check
        if kwargs.get('health_check'):
            return []
        
        if not isinstance(data, dict):
            raise ValueError("Data must be a dict with 'articles' and 'query'")
        
        articles = data.get('articles', [])
        query = data.get('query', '')
        top_n = kwargs.get('top_n', 15)
        
        if not articles:
            return []
        
        if not query:
            self.logger.warning("No query provided, returning articles as-is")
            return articles[:top_n]
        
        # Show loading
        spinner = None
        if self.show_loading:
            spinner = LoadingSpinner("⚖️ Ranking by relevance")
            spinner.start()
        
        try:
            ranked = self._rank_with_ai(articles, query, top_n)
            
            if spinner:
                spinner.stop()
            
            self.logger.info(f"Ranked {len(ranked)} articles")
            
            return ranked
            
        except Exception as e:
            if spinner:
                spinner.stop()
            
            self.logger.warning(f"AI ranking failed, using fallback: {e}")
            return articles[:top_n]
    
    def _rank_with_ai(self, articles: List[Dict], query: str, top_n: int) -> List[Dict]:
        """Rank articles using AI"""
        
        # Prepare article summaries for AI
        article_summaries = []
        for i, art in enumerate(articles[:30], 1):  # Limit to 30 for AI
            title = art.get('title', '')[:100]
            desc = art.get('description', '')[:100]
            article_summaries.append(f"{i}. {title} - {desc}")
        
        prompt = f"""
User query: "{query}"

Rank these articles by relevance (most to least relevant).
Return ONLY a JSON array of article numbers in order: [5, 2, 8, 1, ...]
Include the top {top_n} most relevant articles.

Articles:
{chr(10).join(article_summaries)}
"""
        
        # Get AI ranking
        response = self.model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean JSON response
        result_text = re.sub(r'```json\s*|\s*```', '', result_text)
        
        ranked_indices = json.loads(result_text)
        
        # Build ranked article list
        ranked_articles = []
        for idx in ranked_indices:
            if 1 <= idx <= len(articles):
                article = articles[idx - 1].copy()
                article['relevance_rank'] = len(ranked_articles) + 1
                ranked_articles.append(article)
        
        return ranked_articles[:top_n]