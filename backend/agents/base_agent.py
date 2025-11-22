"""
Base Agent Class
Foundation for all specialized agents in the multi-agent system
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseAgent(ABC):
    """
    Base class for all agents
    Provides common functionality and interface
    """
    
    def __init__(self, name: str, show_loading: bool = True):
        """
        Initialize base agent
        
        Args:
            name: Agent name for logging
            show_loading: Whether to show loading indicators
        """
        self.name = name
        self.show_loading = show_loading
        self.logger = logging.getLogger(f"MultiAgent.{name}")
        
        # Metrics
        self.metrics = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'total_time': 0.0,
            'avg_time': 0.0,
        }
        
        self.logger.info(f"{name} agent initialized")
    
    @abstractmethod
    def process(self, data: Any, **kwargs) -> Any:
        """
        Main processing method - must be implemented by subclasses
        
        Args:
            data: Input data to process
            **kwargs: Additional parameters
            
        Returns:
            Processed result
        """
        pass
    
    def execute(self, data: Any, **kwargs) -> Dict[str, Any]:
        """
        Execute agent with error handling and metrics
        
        Args:
            data: Input data
            **kwargs: Additional parameters
            
        Returns:
            Dict with keys: success, data, error, time
        """
        start_time = time.time()
        self.metrics['total_calls'] += 1
        
        try:
            self.logger.debug(f"{self.name} starting execution")
            
            result = self.process(data, **kwargs)
            
            elapsed = time.time() - start_time
            self.metrics['successful_calls'] += 1
            self.metrics['total_time'] += elapsed
            self.metrics['avg_time'] = self.metrics['total_time'] / self.metrics['total_calls']
            
            self.logger.debug(f"{self.name} completed in {elapsed:.2f}s")
            
            return {
                'success': True,
                'data': result,
                'error': None,
                'time': elapsed,
                'agent': self.name
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.metrics['failed_calls'] += 1
            self.metrics['total_time'] += elapsed
            self.metrics['avg_time'] = self.metrics['total_time'] / self.metrics['total_calls']
            
            self.logger.error(f"{self.name} failed: {e}")
            
            return {
                'success': False,
                'data': None,
                'error': str(e),
                'time': elapsed,
                'agent': self.name
            }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics"""
        success_rate = (
            self.metrics['successful_calls'] / self.metrics['total_calls'] * 100
            if self.metrics['total_calls'] > 0 else 0
        )
        
        return {
            'name': self.name,
            'total_calls': self.metrics['total_calls'],
            'successful_calls': self.metrics['successful_calls'],
            'failed_calls': self.metrics['failed_calls'],
            'success_rate': f"{success_rate:.2f}%",
            'avg_time': f"{self.metrics['avg_time']:.2f}s",
            'total_time': f"{self.metrics['total_time']:.2f}s"
        }
    
    def reset_metrics(self):
        """Reset agent metrics"""
        self.metrics = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'total_time': 0.0,
            'avg_time': 0.0,
        }
        self.logger.info(f"{self.name} metrics reset")
    
    def health_check(self) -> Dict[str, Any]:
        """Check agent health"""
        try:
            # Simple health check - can be overridden
            test_result = self.process(None, health_check=True)
            return {
                'agent': self.name,
                'status': 'healthy',
                'timestamp': datetime.now().isoformat()
            }
        except:
            return {
                'agent': self.name,
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat()
            }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"