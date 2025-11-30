import { useState, useRef } from 'react';
import { ChatInterface } from '@/components/ChatInterface';
import { NewsPreview } from '@/components/NewsPreview';
import { mockNewsArticles } from '@/data/mockNews';

interface Message {
  id: string;
  type: 'user' | 'ai' | 'loading';
  text?: string;
  timestamp: Date;
  newsTitles?: Array<{ id: string; title: string }>;
}

interface NewsArticle {
  id: string;
  title: string;
  description: string;
  source: string;
  publishedAt: Date;
  imageUrl: string;
  url: string;
}

function Index() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messageIdCounter = useRef(0);

  const scrollToArticle = (articleId: string) => {
    const element = document.getElementById(`article-${articleId}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };


  const handleSendMessage = async (text: string) => {

  const userMessage: Message = {
    id: `msg-${messageIdCounter.current++}`,
    type: 'user',
    text,
    timestamp: new Date(),
  };

  const loadingMessage: Message = {
    id: `msg-${messageIdCounter.current++}`,
    type: 'loading',
    timestamp: new Date(),
  };

  setMessages((prev) => [...prev, userMessage, loadingMessage]);
  setIsLoading(true);

  try {
    const response = await fetch('http://localhost:8000/api/news/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: text,
        max_results: 5,
        enrich: true,
        parallel: true
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch news');
    }

    const data = await response.json();

    if (!data.success) {
      throw new Error(data.message || 'Failed to fetch news');
    }

    const fetchedArticles: NewsArticle[] = await Promise.all(
      data.articles.map(async (article: any, index: number) => {
        let enrichedData = {
          imageUrl: article.image_url || null,
          description: article.description || article.summary || null,
        };

        if (article.url) {
          try {
            const previewResponse = await fetch(
              `http://localhost:8000/api/news/preview?url=${encodeURIComponent(article.url)}`
            );
            if (previewResponse.ok) {
              const previewData = await previewResponse.json();
              enrichedData = {
                imageUrl: previewData.image || enrichedData.imageUrl,
                description: previewData.preview_text || enrichedData.description,
              };
            }
          } catch (error) {
            console.log('Preview fetch failed for:', article.url);
          }
        }

        return {
          id: `article-${Date.now()}-${index}`,
          title: article.title || 'Untitled',
          description: enrichedData.description || 'No description available',
          source: article.source || 'Unknown Source',
          publishedAt: article.published_date ? new Date(article.published_date) : new Date(),
          imageUrl: enrichedData.imageUrl || 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800',
          url: article.url || '#',
        };
      })
    );


    const newsTitles = fetchedArticles.map((article) => ({
      id: article.id,
      title: article.title,
    }));

    const aiMessage: Message = {
      id: `msg-${messageIdCounter.current++}`,
      type: 'ai',
      text: `Found ${fetchedArticles.length} articles about "${text}":`,
      timestamp: new Date(),
      newsTitles,
    };

    setMessages((prev) => [
      ...prev.filter((msg) => msg.type !== 'loading'),
      aiMessage
    ]);

    setArticles((prev) => [...prev, ...fetchedArticles]);

  } catch (error) {
    console.error('Error fetching news:', error);

    const errorMessage: Message = {
      id: `msg-${messageIdCounter.current++}`,
      type: 'ai',
      text: 'Sorry, I encountered an error while fetching news. Please make sure the API server is running on localhost:8000.',
      timestamp: new Date(),
    };

    setMessages((prev) => [
      ...prev.filter((msg) => msg.type !== 'loading'),
      errorMessage
    ]);

  } finally {
    setIsLoading(false);
  }
};

  return (
    <div className="flex flex-col lg:flex-row h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">

      <div className="w-full lg:w-2/5 border-r border-gray-700 flex flex-col h-full lg:h-full">
        <ChatInterface
        isLoading={isLoading}
          messages={messages}
          onSendMessage={handleSendMessage}
          onTitleClick={scrollToArticle}
        />
      </div>

      <div className="hidden lg:block lg:w-3/5 overflow-y-auto h-full">
        <NewsPreview isLoading={isLoading} articles={articles} />
      </div>
    </div>
  );

}

export default Index;