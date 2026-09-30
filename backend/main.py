import sys
import time
from typing import List, Dict
from datetime import datetime
import random

from services.orchestrator import MultiAgentOrchestrator
from config import Config


class ConversationalMultiAgentNews:
    """Chat interface for multi-agent news system"""
    
    def __init__(self):
        """Initialize multi-agent system"""
        print("🚀 Initializing Multi-Agent News System...")
        print("   ├─ QueryAgent")
        print("   ├─ GoogleNewsAgent")
        print("   ├─ RSSFeedAgent")
        print("   ├─ ContentAgent")
        print("   ├─ RankingAgent")
        print("   └─ SummaryAgent")
        print()
        
        self.orchestrator = MultiAgentOrchestrator(
            api_key=Config.GOOGLE_AI_STUDIO_KEY,
            show_loading=True
        )
        
        self.session_start = datetime.now()
        self.last_query = None
        self.last_results = []
        
        self.user_preferences = {
            'num_results': 5,
            'show_summaries': True,
            'detail_level': 'medium',
            'parallel_processing': True
        }
        
        print("✅ Multi-Agent System Ready!\n")
    
    def handle_greeting(self) -> str:
        """Handle greeting"""
        greetings = [
            "👋 Hello! I'm your Multi-Agent AI News Assistant with 6 specialized agents!",
            "🤖 Hi! My agent team is ready to find the best news for you!",
            "👋 Hey! Using parallel processing with multiple AI agents to get you the best results!",
        ]
        return random.choice(greetings)
    
    def handle_help(self) -> str:
        """Show help"""
        return """
🤖 **Multi-Agent News System**

📰 **Get News:** Just ask naturally!
   • "Latest AI news"
   • "What's happening in India?"
   • "Technology developments"

🔍 **Commands:**
   • Type any news topic to search
   • "more" - Show more articles
   • "stats" - View system & agent stats
   • "agents" - View agent status
   • "parallel on/off" - Toggle parallel processing
   • "bye" - Exit

💡 **System Features:**
   • 6 specialized AI agents working together
   • Parallel search for 2-3x faster results
   • AI-powered ranking and summarization
   • Fault-tolerant architecture

What would you like to know about?
"""
    
    def handle_news_query(self, query: str) -> str:
        """Handle news query with multi-agent system"""
        self.last_query = query
        
        # Check if user specified a number in query
        # The QueryAgent will extract it automatically
        
        # Use multi-agent orchestrator
        response = self.orchestrator.fetch_news(
            query=query,
            max_results=self.user_preferences['num_results'],  # Default
            enrich=True,
            parallel=self.user_preferences['parallel_processing']
        )
        
        if not response['success']:
            return f"❌ Sorry: {response['message']}"
        
        self.last_results = response['data']
        articles = response['data']
        
        # Update user preference based on what was delivered
        actual_count = len(articles)
        if actual_count > self.user_preferences['num_results']:
            self.user_preferences['num_results'] = actual_count
        
        # Build response
        output = "\n📰 **YOUR MULTI-AGENT NEWS RESULTS:**\n"
        output += "─" * 70 + "\n"
        
        for i, article in enumerate(articles, 1):
            output += f"\n🔹 **Article {i}**"
            
            # Show which agent fetched it
            if 'agent' in article:
                output += f" (via {article['agent']})"
            
            output += f"\n📌 {article['title']}\n"
            output += f"📍 {article['source']} • {article['published']}\n"
            
            if self.user_preferences['show_summaries']:
                summary = article.get('full_summary', article.get('description', ''))
                if self.user_preferences['detail_level'] == 'brief':
                    summary = summary[:150] + "..."
                output += f"\n💡 {summary}\n"
            
            output += f"🔗 {article['url']}\n"
            output += "─" * 70 + "\n"
        
        # Show metrics
        metrics = response['metrics']
        output += f"\n⚡ Response time: {metrics['response_time']}"
        output += f" | 📊 Delivered: {len(articles)} articles"
        output += f" | 🔄 Parallel: {'✅' if self.user_preferences['parallel_processing'] else '❌'}"
        output += "\n💬 Type 'more' for more articles or 'stats' for detailed metrics!"
        
        return output
    
    def handle_more(self) -> str:
        """Show more results"""
        if not self.last_query:
            return "❌ No previous query. Ask me something first!"
        
        self.user_preferences['num_results'] += 3
        return self.handle_news_query(self.last_query)
    
    def handle_stats(self) -> str:
        """Show statistics"""
        system_metrics = self.orchestrator.get_system_metrics()
        agent_metrics = self.orchestrator.get_agent_metrics()
        
        session_duration = datetime.now() - self.session_start
        minutes = int(session_duration.total_seconds() / 60)
        
        output = "\n📊 **MULTI-AGENT SYSTEM STATISTICS**\n"
        output += "═" * 70 + "\n"
        
        # System stats
        output += "\n🖥️ **System Metrics:**\n"
        output += f"   ⏱️  Session duration: {minutes} minutes\n"
        output += f"   🔍 Total requests: {system_metrics['total_requests']}\n"
        output += f"   ✅ Success rate: {system_metrics['success_rate']}\n"
        output += f"   📰 Articles delivered: {system_metrics['total_articles_delivered']}\n"
        
        # Agent stats
        output += "\n🤖 **Agent Performance:**\n"
        for agent_name, metrics in agent_metrics.items():
            output += f"\n   {agent_name}:\n"
            output += f"      Calls: {metrics['total_calls']} | "
            output += f"Success: {metrics['success_rate']} | "
            output += f"Avg Time: {metrics['avg_time']}\n"
        
        output += "═" * 70 + "\n"
        return output
    
    def handle_agents(self) -> str:
        """Show agent status"""
        health = self.orchestrator.health_check()
        
        output = "\n🤖 **AGENT STATUS**\n"
        output += "═" * 70 + "\n"
        output += f"System Status: {health['system'].upper()}\n\n"
        
        for agent_name, status in health['agents'].items():
            emoji = "✅" if status == "healthy" else "❌"
            output += f"   {emoji} {agent_name}: {status}\n"
        
        output += "═" * 70 + "\n"
        return output
    
    def handle_parallel(self, mode: str) -> str:
        """Toggle parallel processing"""
        if mode == 'on':
            self.user_preferences['parallel_processing'] = True
            return "✅ Parallel processing enabled! Searches will be faster."
        elif mode == 'off':
            self.user_preferences['parallel_processing'] = False
            return "⚠️ Parallel processing disabled. Searches will be sequential."
        else:
            current = "ON" if self.user_preferences['parallel_processing'] else "OFF"
            return f"Current mode: {current}\nUsage: 'parallel on' or 'parallel off'"
    
    def handle_exit(self) -> str:
        """Handle exit"""
        stats = self.handle_stats()
        return f"{stats}\n👋 Thanks for using Multi-Agent News System! Goodbye! 🌟"
    
    def chat(self, user_input: str) -> str:
        """Main chat handler"""
        user_input_lower = user_input.lower().strip()
        
        # Route commands
        if user_input_lower in ['hi', 'hello', 'hey', 'namaste']:
            return self.handle_greeting()
        
        elif user_input_lower in ['help', 'commands']:
            return self.handle_help()
        
        elif user_input_lower in ['more', 'next']:
            return self.handle_more()
        
        elif user_input_lower in ['stats', 'metrics']:
            return self.handle_stats()
        
        elif user_input_lower in ['agents', 'status', 'health']:
            return self.handle_agents()
        
        elif user_input_lower.startswith('parallel'):
            parts = user_input_lower.split()
            mode = parts[1] if len(parts) > 1 else None
            return self.handle_parallel(mode)
        
        else:
            # Default to news query
            return self.handle_news_query(user_input)


def print_banner():
    """Print startup banner"""
    print("\n" + "═" * 80)
    print("🚀 MULTI-AGENT AI NEWS SYSTEM")
    print("═" * 80)
    print("🤖 6 Specialized Agents Working Together:")
    print("   • QueryAgent - Understands your intent")
    print("   • GoogleNewsAgent - Searches Google News")
    print("   • RSSFeedAgent - Fetches from RSS feeds")
    print("   • ContentAgent - Extracts full articles")
    print("   • RankingAgent - Ranks by relevance")
    print("   • SummaryAgent - Generates AI summaries")
    print("\n⚡ Features:")
    print("   • Parallel processing for 2-3x speed")
    print("   • Fault-tolerant architecture")
    print("   • Individual agent metrics")
    print("\n💡 Type 'help' for commands, 'bye' to exit")
    print("═" * 80 + "\n")


def main():
    """Main chat loop"""
    try:
        # Initialize system
        agent = ConversationalMultiAgentNews()
        
        # Show banner
        print_banner()
        
        # Greeting
        print(f"🤖: {agent.handle_greeting()}\n")
        
        # Chat loop
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['bye', 'exit', 'quit', 'goodbye']:
                    print(f"\n🤖: {agent.handle_exit()}")
                    break
                
                print()
                response = agent.chat(user_input)
                print(f"🤖: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Interrupted!")
                print(f"🤖: {agent.handle_exit()}")
                break
            
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Let's try again...\n")
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()