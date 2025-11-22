"""
Enhanced Test Script - Shows full URLs and comprehensive summaries
"""

from services.enhanced_fetch import EnhancedNewsFetcher
from config import Config
import sys

def display_article_full(article: dict, index: int):
    """Display article with all details"""
    print(f"\n{'─'*80}")
    print(f"📰 ARTICLE {index}")
    print(f"{'─'*80}")
    print(f"\n📌 Title: {article['title']}")
    print(f"\n🔗 Full URL: {article['url']}")
    print(f"\n📍 Source: {article['source']}")
    print(f"📅 Published: {article['published']}")
    
    if article.get('authors'):
        print(f"✍️  Authors: {', '.join(article['authors'])}")
    
    print(f"\n📝 Comprehensive Summary:")
    print("-" * 80)
    summary = article.get('full_summary', article.get('description', 'No summary available'))
    print(summary)
    
    if article.get('full_text'):
        print(f"\n📄 Article Preview (first 300 chars):")
        print("-" * 80)
        print(article['full_text'][:300] + "...")
    
    print(f"\n🔧 Fetch Method: {article.get('fetch_method', 'unknown')}")
    print("─" * 80)


def test_enhanced_fetcher():
    """Test the enhanced fetcher"""
    print("\n" + "="*80)
    print("🧪 TESTING ENHANCED NEWS AGGREGATOR")
    print("="*80 + "\n")
    
    try:
        Config.validate()
        print("✅ Configuration valid\n")
    except ValueError as e:
        print(f"❌ Configuration error: {e}\n")
        return False
    
    try:
        fetcher = EnhancedNewsFetcher(Config.GOOGLE_AI_STUDIO_KEY)
        print("✅ Enhanced fetcher initialized\n")
    except Exception as e:
        print(f"❌ Initialization error: {e}\n")
        return False
    
    # Test queries
    test_queries = [
        "AI news from India",
        "Technology developments today",
        "Cybersecurity news"
    ]
    
    print("Choose a test query:")
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. {query}")
    print("4. Enter custom query")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice in ['1', '2', '3']:
        query = test_queries[int(choice) - 1]
    elif choice == '4':
        query = input("Enter your query: ").strip()
    else:
        print("Invalid choice")
        return False
    
    print(f"\n{'='*80}")
    print(f"🔍 Testing with query: '{query}'")
    print(f"{'='*80}\n")
    
    try:
        # Fetch with full enrichment
        results = fetcher.fetch_news(query, max_results=5, enrich=True)
        
        if results:
            print("\n" + "="*80)
            print(f"✅ SUCCESSFULLY FETCHED {len(results)} ENRICHED ARTICLES")
            print("="*80)
            
            # Display all articles with full details
            for i, article in enumerate(results, 1):
                display_article_full(article, i)
                
                if i < len(results):
                    input("\n[Press Enter to see next article...]")
            
            print("\n" + "="*80)
            print("✅ TEST COMPLETED SUCCESSFULLY!")
            print("="*80 + "\n")
            
            # Summary statistics
            print("📊 SUMMARY:")
            print(f"  • Total articles fetched: {len(results)}")
            print(f"  • Articles with full summaries: {sum(1 for a in results if a.get('full_summary'))}")
            print(f"  • Articles with authors: {sum(1 for a in results if a.get('authors'))}")
            print(f"  • Unique sources: {len(set(a['source'] for a in results))}")
            
            sources = {}
            for article in results:
                source = article['source']
                sources[source] = sources.get(source, 0) + 1
            
            print(f"\n  📡 Sources breakdown:")
            for source, count in sources.items():
                print(f"     - {source}: {count} article(s)")
            
        else:
            print("⚠️  No articles fetched")
            
    except Exception as e:
        print(f"❌ Error during fetch: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def interactive_mode():
    """Interactive testing mode"""
    print("\n" + "="*80)
    print("🎮 ENHANCED INTERACTIVE MODE")
    print("="*80 + "\n")
    
    try:
        Config.validate()
        fetcher = EnhancedNewsFetcher(Config.GOOGLE_AI_STUDIO_KEY)
        
        while True:
            print("\n" + "-"*80)
            query = input("Enter your news query (or 'quit' to exit): ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                print("⚠️  Please enter a valid query")
                continue
            
            num_results = input("How many articles? (default 5): ").strip()
            try:
                num_results = int(num_results) if num_results else 5
            except:
                num_results = 5
            
            try:
                results = fetcher.fetch_news(query, max_results=num_results, enrich=True)
                
                if results:
                    for i, article in enumerate(results, 1):
                        display_article_full(article, i)
                        
                        if i < len(results):
                            cont = input("\n[Press Enter for next article, 's' to skip, 'q' to quit]: ").strip().lower()
                            if cont == 'q':
                                break
                            elif cont == 's':
                                continue
                else:
                    print("⚠️  No articles found")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main test runner"""
    print("\n🤖 Enhanced Smart News Aggregator - Test Suite\n")
    print("Choose an option:")
    print("1. Run single test with sample query")
    print("2. Interactive mode (test with multiple custom queries)")
    
    choice = input("\nEnter choice (1/2): ").strip()
    
    if choice == '1':
        test_enhanced_fetcher()
    elif choice == '2':
        interactive_mode()
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)