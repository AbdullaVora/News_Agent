"""
Multi-Agent Orchestrator
Coordinates all specialized agents to fetch and process news
"""

import logging
import time
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Import all agents
import sys
sys.path.append('agents')

from agents.query_agent import QueryAgent
from agents.google_news_agent import GoogleNewsAgent
from agents.rss_feed_agent import RSSFeedAgent
from agents.content_agent import ContentAgent
from agents.ranking_agent import RankingAgent
from agents.summary_agent import SummaryAgent


class MultiAgentOrchestrator:
    """
    Orchestrates multiple specialized agents for news fetching
    Provides parallel processing and fault tolerance
    """
    
    def __init__(self, api_key: str, show_loading: bool = True):
        """
        Initialize orchestrator with all agents
        
        Args:
            api_key: Google AI Studio API key
            show_loading: Show loading animations
        """
        self.logger = logging.getLogger("MultiAgent.Orchestrator")
        self.show_loading = show_loading
        
        self.logger.info("Initializing Multi-Agent System...")
        
        # Initialize all agents
        self.agents = {
            'query': QueryAgent(api_key, show_loading),
            'google_news': GoogleNewsAgent(show_loading),
            'rss_feed': RSSFeedAgent(show_loading),
            'content': ContentAgent(show_loading),
            'ranking': RankingAgent(api_key, show_loading),
            'summary': SummaryAgent(api_key, show_loading),
        }
        
        # System metrics
        self.system_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'avg_response_time': 0.0,
            'total_articles_delivered': 0,
        }
        
        self.logger.info("✅ Multi-Agent System Ready!")
        self.logger.info(f"Active agents: {list(self.agents.keys())}")
    
    def fetch_news(
        self, 
        query: str, 
        max_results: int = 10,
        enrich: bool = True,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Fetch news using multi-agent system
        
        Args:
            query: User query
            max_results: Maximum results to return (default, can be overridden by query)
            enrich: Whether to enrich with summaries
            parallel: Use parallel processing for search agents
            
        Returns:
            Dict with success, data, metrics, agent_stats
        """
        start_time = time.time()
        self.system_metrics['total_requests'] += 1
        
        try:
            self.logger.info(f"Processing query: {query}")
            
            # ==========================================
            # STEP 1: UNDERSTAND QUERY
            # ==========================================
            if self.show_loading:
                print(f"\n{'='*70}")
                print(f"🔍 Multi-Agent Search: {query}")
                print(f"{'='*70}\n")
            
            query_result = self.agents['query'].execute(query)
            
            if not query_result['success']:
                raise Exception(f"Query parsing failed: {query_result['error']}")
            
            intent = query_result['data']
            
            # Override max_results if user specified a number
            if intent.get('max_results'):
                max_results = intent['max_results']
                self.logger.info(f"Using user-requested count: {max_results}")
            
            # ==========================================
            # STEP 2: PARALLEL SEARCH (Google News + RSS)
            # ==========================================
            all_articles = []
            
            if parallel:
                # Parallel execution
                all_articles = self._parallel_search(intent)
            else:
                # Sequential execution
                all_articles = self._sequential_search(intent)
            
            if not all_articles:
                return self._create_response(
                    success=False,
                    data=[],
                    message="No articles found",
                    start_time=start_time
                )
            
            self.logger.info(f"Total articles collected: {len(all_articles)}")
            
            # ==========================================
            # STEP 3: RANK BY RELEVANCE
            # ==========================================
            ranking_result = self.agents['ranking'].execute({
                'articles': all_articles,
                'query': query
            }, top_n=max_results * 2)  # Get more for filtering
            
            if not ranking_result['success']:
                self.logger.warning("Ranking failed, using unranked articles")
                ranked_articles = all_articles[:max_results * 2]
            else:
                ranked_articles = ranking_result['data']
            
            # ==========================================
            # STEP 4: EXTRACT CONTENT (if enrich)
            # ==========================================
            if enrich:
                content_result = self.agents['content'].execute(
                    ranked_articles,
                    max_to_extract=max_results
                )
                
                if content_result['success']:
                    articles_with_content = content_result['data']
                else:
                    self.logger.warning("Content extraction failed")
                    articles_with_content = ranked_articles[:max_results]
            else:
                articles_with_content = ranked_articles[:max_results]
            
            # ==========================================
            # STEP 5: GENERATE SUMMARIES (if enrich)
            # ==========================================
            if enrich:
                summary_result = self.agents['summary'].execute(
                    articles_with_content,
                    max_to_summarize=max_results
                )
                
                if summary_result['success']:
                    final_articles = summary_result['data']
                else:
                    self.logger.warning("Summary generation failed")
                    final_articles = articles_with_content
            else:
                final_articles = articles_with_content
            
            # ==========================================
            # FINALIZE
            # ==========================================
            elapsed = time.time() - start_time
            
            self.system_metrics['successful_requests'] += 1
            self.system_metrics['total_articles_delivered'] += len(final_articles)
            
            return self._create_response(
                success=True,
                data=final_articles,
                message=f"Successfully fetched {len(final_articles)} articles",
                start_time=start_time
            )
        
        except Exception as e:
            self.logger.error(f"Orchestrator error: {e}")
            self.system_metrics['failed_requests'] += 1
            
            elapsed = time.time() - start_time
            
            return self._create_response(
                success=False,
                data=[],
                message=f"Error: {str(e)}",
                start_time=start_time
            )
    
    def _parallel_search(self, intent: Dict) -> List[Dict]:
        """Execute search agents in parallel"""
        
        all_articles = []
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit Google News search
            google_future = executor.submit(
                self.agents['google_news'].execute,
                {
                    'search_term': intent['search_term'],
                    'location': intent.get('location')
                },
                max_results=10
            )
            
            # Submit RSS search
            rss_future = executor.submit(
                self.agents['rss_feed'].execute,
                {
                    'category': intent['category']
                },
                max_results_per_feed=8
            )
            
            # Collect results
            for future in as_completed([google_future, rss_future]):
                try:
                    result = future.result(timeout=30)
                    if result['success']:
                        all_articles.extend(result['data'])
                except Exception as e:
                    self.logger.warning(f"Search agent failed: {e}")
        
        return all_articles
    
    def _sequential_search(self, intent: Dict) -> List[Dict]:
        """Execute search agents sequentially"""
        
        all_articles = []
        
        # Google News
        google_result = self.agents['google_news'].execute({
            'search_term': intent['search_term'],
            'location': intent.get('location')
        }, max_results=10)
        
        if google_result['success']:
            all_articles.extend(google_result['data'])
        
        # RSS Feeds
        rss_result = self.agents['rss_feed'].execute({
            'category': intent['category']
        }, max_results_per_feed=8)
        
        if rss_result['success']:
            all_articles.extend(rss_result['data'])
        
        return all_articles
    
    def _create_response(
        self, 
        success: bool, 
        data: List[Dict], 
        message: str,
        start_time: float
    ) -> Dict[str, Any]:
        """Create standardized response"""
        
        elapsed = time.time() - start_time
        
        return {
            'success': success,
            'data': data,
            'message': message,
            'metrics': {
                'response_time': f"{elapsed:.2f}s",
                'num_articles': len(data),
                'parallel_processing': True
            },
            'agent_stats': self.get_agent_metrics()
        }
    
    def get_agent_metrics(self) -> Dict[str, Any]:
        """Get metrics from all agents"""
        
        metrics = {}
        
        for name, agent in self.agents.items():
            metrics[name] = agent.get_metrics()
        
        return metrics
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get overall system metrics"""
        
        return {
            'total_requests': self.system_metrics['total_requests'],
            'successful_requests': self.system_metrics['successful_requests'],
            'failed_requests': self.system_metrics['failed_requests'],
            'success_rate': f"{(self.system_metrics['successful_requests'] / max(1, self.system_metrics['total_requests']) * 100):.2f}%",
            'total_articles_delivered': self.system_metrics['total_articles_delivered'],
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of all agents"""
        
        health = {
            'system': 'healthy',
            'agents': {}
        }
        
        for name, agent in self.agents.items():
            agent_health = agent.health_check()
            health['agents'][name] = agent_health['status']
            
            if agent_health['status'] != 'healthy':
                health['system'] = 'degraded'
        
        return health