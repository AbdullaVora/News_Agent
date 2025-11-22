"""
AI News Agent with Thinking Animation - Complete Single File
Just run: python main.py

Requirements: Same as before (feedparser, newspaper3k, google-generativeai, etc.)
"""

import sys
import time
from typing import List, Dict, Optional
from datetime import datetime
import random

# Import your existing modules
from services.enhanced_fetch import EnhancedNewsFetcher
from agents.agent import ProductionNewsAgent
from config import Config


# ============================================
# THINKING ANIMATION CLASS
# ============================================

class AgentThinkingAnimation:
    """Visual animation for AI agent thinking process"""
    
    def __init__(self):
        self.steps_completed = []
    
    def animate_text(self, text: str, delay: float = 0.03):
        """Animate text character by character"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def show_spinner(self, message: str, duration: float = 1.5):
        """Show animated spinner"""
        spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            sys.stdout.write(f'\r{spinners[i % len(spinners)]} {message}')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        sys.stdout.write('\r' + ' ' * (len(message) + 3) + '\r')
        sys.stdout.flush()
    
    def thinking_step(self, emoji: str, message: str, substeps: List[str] = None, thinking_time: float = 1.0):
        """Display a thinking step with animation"""
        print(f"{emoji} {message}")
        self.show_spinner(message, thinking_time)
        
        # Only show substeps if provided (we won't provide them anymore)
        if substeps:
            for substep in substeps:
                print(f"   ├─ {substep}")
                time.sleep(0.3)
            print(f"   └─ ✓")
        
        time.sleep(0.1)
        self.steps_completed.append(message)


# ============================================
# THINKING NEWS AGENT
# ============================================

class ThinkingNewsAgent:
    """News agent with visual thinking process"""
    
    def __init__(self, base_agent):
        self.agent = base_agent
        self.animator = AgentThinkingAnimation()
    
    def fetch_with_thinking(self, query: str, max_results: int = 5) -> dict:
        """Fetch news with full thinking animation"""
        
        print("\n" + "═" * 80)
        print("🤖 AI AGENT THINKING...")
        print("═" * 80 + "\n")
        
        # Step 1: Understanding query
        self.animator.thinking_step(
            emoji="🧠",
            message="Understanding your request...",
            substeps=None,
            thinking_time=0.8
        )
        
        # Step 2: Planning search
        self.animator.thinking_step(
            emoji="📋",
            message="Planning the best approach...",
            substeps=None,
            thinking_time=0.6
        )
        
        # Step 3: Gathering data
        self.animator.thinking_step(
            emoji="🌐",
            message="Searching across news sources...",
            substeps=None,
            thinking_time=1.0
        )
        
        # Actual fetch
        self.animator.thinking_step(
            emoji="⚡",
            message="EXECUTING SEARCH...",
            substeps=None,
            thinking_time=2.0  # Longer spinner for actual search
        )
        
        response = self.agent.fetch_news(
            query=query,
            max_results=max_results,
            enrich=True,
            use_cache=True
        )
        
        if not response['success']:
            print("❌ Search failed!\n")
            return response
        
        # Step 4: Processing results
        self.animator.thinking_step(
            emoji="🔍",
            message="Analyzing the findings...",
            substeps=None,
            thinking_time=0.8
        )
        
        # Step 5: AI Summary generation
        self.animator.thinking_step(
            emoji="🤖",
            message="Generating intelligent summaries...",
            substeps=None,
            thinking_time=1.0
        )
        
        # Step 6: Ranking
        self.animator.thinking_step(
            emoji="⚖️",
            message="Ranking by relevance...",
            substeps=None,
            thinking_time=0.6
        )
        
        # Step 7: Final preparation
        self.animator.thinking_step(
            emoji="📦",
            message="Preparing your results...",
            substeps=None,
            thinking_time=0.5
        )
        
        # Completion
        print("\n" + "═" * 80)
        print(f"✅ DONE! Found {len(response['data'])} articles")
        print("═" * 80)
        
        cache_status = "💾 FROM CACHE" if response['from_cache'] else "🆕 FRESH FETCH"
        print(f"\n⏱️  Total time: {response['metrics']['response_time']}")
        print(f"📊 Status: {cache_status}")
        print(f"📰 Articles found: {response['metrics']['num_articles']}")
        print("\n" + "═" * 80 + "\n")
        
        return response


# ============================================
# CONVERSATIONAL AGENT WITH THINKING
# ============================================

class ConversationalNewsAgent:
    """Chat-style news agent with thinking animation"""
    
    def __init__(self):
        """Initialize"""
        print("🔧 Initializing AI components...")
        
        self.base_agent = ProductionNewsAgent(
            api_key=Config.GOOGLE_AI_STUDIO_KEY,
            cache_ttl_minutes=30,
            rate_limit_requests=15,
            rate_limit_window=60,
            log_level="WARNING"
        )
        
        self.thinking_agent = ThinkingNewsAgent(self.base_agent)
        
        self.conversation_history = []
        self.session_start = datetime.now()
        self.last_query = None
        self.last_results = []
        
        self.user_preferences = {
            'num_results': 5,
            'show_summaries': True,
            'detail_level': 'medium'
        }
        
        print("✅ Agent initialized!\n")
    
    def handle_greeting(self) -> str:
        """Handle greeting"""
        greetings = [
            "👋 Hello! I'm your AI news assistant. What would you like to know about today?",
            "🤖 Hi there! Ask me about any news topic and I'll find the latest articles for you!",
            "👋 Hey! Ready to catch up on the latest news? What interests you?",
        ]
        return random.choice(greetings)
    
    def handle_help(self) -> str:
        """Show help"""
        return """
🤖 **How I can help you:**

📰 **Get News:** Just ask naturally!
   • "Latest AI news"
   • "What's happening in India today?"
   • "Tell me about cryptocurrency"
   • "Technology developments this week"

🔍 **Commands:**
   • Type any news topic to search
   • "more" - Show more articles
   • "stats" - View performance stats
   • "bye" - Exit chat

💡 **Tips:**
   • I show my complete thinking process!
   • I understand natural language
   • I cache results for faster responses

What would you like to know about?
"""
    
    def handle_news_query(self, query: str) -> str:
        """Handle news query with thinking"""
        self.last_query = query
        
        # Use thinking agent
        response = self.thinking_agent.fetch_with_thinking(
            query=query,
            max_results=self.user_preferences['num_results']
        )
        
        if not response['success']:
            return f"❌ Sorry: {response['message']}"
        
        self.last_results = response['data']
        articles = response['data']
        
        # Build response
        output = "\n📰 **YOUR NEWS RESULTS:**\n"
        output += "─" * 70 + "\n"
        
        for i, article in enumerate(articles, 1):
            output += f"\n🔹 **Article {i}**\n"
            output += f"📌 {article['title']}\n"
            output += f"📍 {article['source']} • {article['published']}\n"
            
            if self.user_preferences['show_summaries']:
                summary = article.get('full_summary', article.get('description', ''))
                if self.user_preferences['detail_level'] == 'brief':
                    summary = summary[:150] + "..."
                output += f"\n💡 {summary}\n"
            
            output += f"🔗 {article['url']}\n"
            output += "─" * 70 + "\n"
        
        output += "\n💬 Type 'more' for more articles!"
        return output
    
    def handle_more(self) -> str:
        """Show more results"""
        if not self.last_query:
            return "❌ No previous query. Ask me something first!"
        
        self.user_preferences['num_results'] += 3
        return self.handle_news_query(self.last_query)
    
    def handle_stats(self) -> str:
        """Show statistics"""
        metrics = self.base_agent.get_metrics()
        session_duration = datetime.now() - self.session_start
        minutes = int(session_duration.total_seconds() / 60)
        
        output = "\n📊 **Agent Statistics:**\n"
        output += "─" * 50 + "\n"
        output += f"⏱️  Session duration: {minutes} minutes\n"
        output += f"🔍 Total queries: {metrics['total_requests']}\n"
        output += f"✅ Success rate: {metrics['success_rate']}\n"
        output += f"💾 Cache hit rate: {metrics['cache_hit_rate']}\n"
        output += f"📰 Articles delivered: {metrics['total_articles_delivered']}\n"
        output += f"⚡ Avg response time: {metrics['avg_response_time']}\n"
        output += "─" * 50 + "\n"
        return output
    
    def handle_exit(self) -> str:
        """Handle exit"""
        stats = self.handle_stats()
        return f"{stats}\n👋 Thanks for using AI News Agent! Goodbye! 🌟"
    
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
        
        else:
            # Default to news query
            return self.handle_news_query(user_input)


# ============================================
# MAIN FUNCTION
# ============================================

def print_banner():
    """Print startup banner"""
    print("\n" + "═" * 80)
    print("🤖 AI LEADER NEWS AGENT - WITH THINKING PROCESS")
    print("═" * 80)
    print("💭 Watch me think, analyze, and reason through your queries")
    print("📰 Get news with full AI intelligence transparency")
    print("🧠 Advanced thinking mode: ACTIVE")
    print("💡 Type 'help' for commands, 'bye' to exit")
    print("═" * 80 + "\n")


def main():
    """Main chat loop"""
    try:
        print("\n🚀 Starting AI News Agent...")
        time.sleep(0.5)
        
        # Initialize agent
        agent = ConversationalNewsAgent()
        
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