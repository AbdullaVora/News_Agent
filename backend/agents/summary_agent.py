"""
Summary Agent
Specializes in generating AI-powered summaries
"""

import time
import sys
import threading
from typing import List, Dict, Any
import google.generativeai as genai

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


class SummaryAgent(BaseAgent):
    """
    Agent specialized in generating intelligent summaries using AI
    """
    
    def __init__(self, api_key: str, show_loading: bool = True):
        """Initialize Summary Agent"""
        super().__init__("SummaryAgent", show_loading)
        
        # Configure AI model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        self.logger.info("AI model configured for summarization")
    
    def process(self, data: Any, **kwargs) -> List[Dict]:
        """
        Generate AI summaries for articles
        
        Args:
            data: List of article dicts
            kwargs: max_to_summarize (default 10)
            
        Returns:
            List of articles with summaries
        """
        # Health check
        if kwargs.get('health_check'):
            return []
        
        if not isinstance(data, list):
            raise ValueError("Data must be a list of article dicts")
        
        max_to_summarize = kwargs.get('max_to_summarize', 10)
        
        # Show loading
        spinner = None
        if self.show_loading:
            spinner = LoadingSpinner("🤖 Generating AI summaries")
            spinner.start()
        
        try:
            summarized = self._generate_summaries(data[:max_to_summarize])
            
            if spinner:
                spinner.stop()
            
            self.logger.info(f"Generated summaries for {len(summarized)} articles")
            
            return summarized
            
        except Exception as e:
            if spinner:
                spinner.stop()
            raise e
    
    def _generate_summaries(self, articles: List[Dict]) -> List[Dict]:
        """Generate summaries for articles"""
        
        summarized = []
        
        for i, article in enumerate(articles, 1):
            try:
                # Check if article has full text content
                full_text = article.get('full_text', '')
                title = article.get('title', '')
                description = article.get('description', '')
                
                # Generate summary
                if full_text and len(full_text) > 100:
                    summary = self._generate_ai_summary(full_text, title)
                elif description:
                    summary = description
                else:
                    summary = "Summary not available."
                
                article['full_summary'] = summary
                article['has_ai_summary'] = bool(full_text and len(full_text) > 100)
                
                summarized.append(article)
                
                # Delay between AI calls
                time.sleep(1)
                
            except Exception as e:
                self.logger.warning(f"Failed to summarize article {i}: {e}")
                article['full_summary'] = article.get('description', 'Summary not available.')
                article['has_ai_summary'] = False
                summarized.append(article)
        
        return summarized
    
    def _generate_ai_summary(self, article_text: str, title: str) -> str:
        """Generate AI summary for article"""
        
        if not article_text or len(article_text) < 100:
            return "Summary not available - insufficient content."
        
        prompt = f"""
Generate a comprehensive 4-5 sentence summary of this news article:

Title: {title}

Article: {article_text[:3000]}

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
            self.logger.warning(f"AI summary generation failed: {e}")
            
            # Fallback: first 3 sentences
            sentences = article_text.split('. ')[:3]
            return '. '.join(sentences) + '.'