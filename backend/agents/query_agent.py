"""
Query Understanding Agent
Specializes in parsing and understanding user queries
"""

import json
import re
from typing import Dict, Any, Optional
import sys
import time
import threading
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
        """Spinner animation loop"""
        while self.is_running:
            sys.stdout.write(f'\r{self.spinners[self.current]} {self.message}...')
            sys.stdout.flush()
            self.current = (self.current + 1) % len(self.spinners)
            time.sleep(0.1)
        
        sys.stdout.write('\r' + ' ' * (len(self.message) + 5) + '\r')
        sys.stdout.flush()
    
    def start(self):
        """Start spinner"""
        self.is_running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop spinner"""
        self.is_running = False
        if self.thread:
            self.thread.join()


class QueryAgent(BaseAgent):
    """
    Agent specialized in understanding user queries
    Extracts: keywords, location, category, intent, requested count
    """
    
    def __init__(self, api_key: str, show_loading: bool = True):
        """Initialize Query Agent"""
        super().__init__("QueryAgent", show_loading)
        
        # Configure AI model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
        self.logger.info("AI model configured for query understanding")
    
    def process(self, data: Any, **kwargs) -> Dict[str, Any]:
        """
        Parse user query and extract structured information
        
        Args:
            data: User query string
            
        Returns:
            Dict with keywords, location, category, search_term, intent, max_results
        """
        # Health check
        if kwargs.get('health_check'):
            return {'status': 'ok'}
        
        query = data
        
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")
        
        # First, extract number from query
        requested_count = self._extract_number_from_query(query)
        
        # Show loading
        spinner = None
        if self.show_loading:
            spinner = LoadingSpinner("🧠 Understanding your query")
            spinner.start()
        
        try:
            # Use AI to parse query
            intent = self._parse_with_ai(query)
            
            # Add requested count
            if requested_count:
                intent['max_results'] = requested_count
                self.logger.info(f"User requested {requested_count} articles")
            else:
                intent['max_results'] = None  # Use default
            
            if spinner:
                spinner.stop()
            
            self.logger.info(f"Parsed query: category={intent['category']}, location={intent.get('location')}, count={intent.get('max_results')}")
            
            return intent
            
        except Exception as e:
            if spinner:
                spinner.stop()
            
            self.logger.warning(f"AI parsing failed, using fallback: {e}")
            
            # Fallback to simple parsing
            fallback = self._fallback_parse(query)
            fallback['max_results'] = requested_count
            return fallback
    
    def _extract_number_from_query(self, query: str) -> Optional[int]:
        """
        Extract number of articles requested from query
        Examples:
        - "10 articles" -> 10
        - "give me 5 news" -> 5
        - "show 20" -> 20
        - "latest 3 news" -> 3
        - "2 news about AI" -> 2
        - "latest AI news" -> None (no number)
        """
        # Pattern to match numbers
        patterns = [
            r'(\d+)\s*(?:articles?|news|results?)',  # "10 articles", "5 news"
            r'(?:give|show|find|get)\s+(?:me\s+)?(\d+)',  # "give me 10", "show 5"
            r'(\d+)\s+(?:latest|recent|top)',  # "10 latest", "3 recent"
            r'(?:latest|recent)?\s*(\d+)\s+(?:news|articles?)',  # "latest 2 news"
            r'^(\d+)\s+',  # "2 AI news" (number at start)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query.lower())
            if match:
                count = int(match.group(1))
                # Validate range (1-50)
                if 1 <= count <= 50:
                    self.logger.debug(f"Extracted count from query: {count}")
                    return count
                elif count > 50:
                    self.logger.warning(f"Requested {count} articles, clamping to 50")
                    return 50
        
        return None
    
    def _parse_with_ai(self, query: str) -> Dict[str, Any]:
        """Parse query using AI"""
        
        prompt = f"""
Analyze this news search query and extract structured information:

Query: "{query}"

Return ONLY a JSON object with these fields:
{{
    "keywords": ["list", "of", "keywords"],
    "location": "country/state/city or null",
    "category": "technology/sports/politics/business/health/entertainment or general",
    "timeframe": "latest/today/recent or null",
    "search_term": "optimized search term for news search",
    "intent": "what the user wants to find"
}}
"""
        
        response = self.model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Clean JSON response
        result_text = re.sub(r'```json\s*|\s*```', '', result_text)
        
        parsed_intent = json.loads(result_text)
        
        return parsed_intent
    
    def _fallback_parse(self, query: str) -> Dict[str, Any]:
        """Simple fallback parsing without AI"""
        
        words = query.lower().split()
        
        # Detect category
        category = 'general'
        if any(word in words for word in ['tech', 'technology', 'ai', 'software']):
            category = 'technology'
        elif any(word in words for word in ['business', 'economy', 'stock', 'market']):
            category = 'business'
        elif any(word in words for word in ['sports', 'cricket', 'football', 'game']):
            category = 'sports'
        elif any(word in words for word in ['politics', 'election', 'government']):
            category = 'politics'
        
        # Try to detect location from common Indian cities
        location = None
        indian_cities = ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata', 
                        'hyderabad', 'pune', 'ahmedabad', 'surat', 'jaipur']
        for city in indian_cities:
            if city in query.lower():
                location = city.title()
                break
        
        return {
            "keywords": words,
            "location": location,
            "category": category,
            "timeframe": "recent",
            "search_term": query,
            "intent": f"Find news about {query}"
        }