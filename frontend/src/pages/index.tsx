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

// function Index() {
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [articles, setArticles] = useState<NewsArticle[]>([]);
//   const [isLoading, setIsLoading] = useState(false);
//   const messageIdCounter = useRef(0);

//   const scrollToArticle = (articleId: string) => {
//     const element = document.getElementById(`article-${articleId}`);
//     if (element) {
//       element.scrollIntoView({ behavior: 'smooth', block: 'start' });
//     }
//   };

//   const handleSendMessage = async (text: string) => {
//     // Add user message
//     const userMessage: Message = {
//       id: `msg-${messageIdCounter.current++}`,
//       type: 'user',
//       text,
//       timestamp: new Date(),
//     };
//     setMessages((prev) => [...prev, userMessage]);

//     // Add loading message
//     const loadingMessage: Message = {
//       id: `msg-${messageIdCounter.current++}`,
//       type: 'loading',
//       timestamp: new Date(),
//     };
//     setMessages((prev) => [...prev, loadingMessage]);

//     setIsLoading(true);

//     try {
//       // Call the API
//       const response = await fetch('http://localhost:8000/api/news/search', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           query: text,
//           max_results: 5,
//           enrich: true,
//           parallel: true
//         }),
//       });

//       if (!response.ok) {
//         throw new Error('Failed to fetch news');
//       }

//       const data = await response.json();

//       // Remove loading message
//       setMessages((prev) => prev.filter((msg) => msg.type !== 'loading'));

//       // Check if the response was successful
//       if (!data.success) {
//         throw new Error(data.message || 'Failed to fetch news');
//       }

//       // Transform API response and enrich with preview data
//       const fetchedArticles: NewsArticle[] = await Promise.all(
//         data.articles.map(async (article: any, index: number) => {
//           let enrichedData = {
//             imageUrl: article.image_url || null,
//             description: article.description || article.summary || null,
//           };

//           // If we have a URL, try to get better preview data from the backend
//           if (article.url) {
//             try {
//               const previewResponse = await fetch(
//                 `http://localhost:8000/api/news/preview?url=${encodeURIComponent(article.url)}`
//               );
//               if (previewResponse.ok) {
//                 const previewData = await previewResponse.json();
//                 enrichedData = {
//                   imageUrl: previewData.image || enrichedData.imageUrl,
//                   description: previewData.preview_text || enrichedData.description,
//                 };
//               }
//             } catch (error) {
//               console.log('Preview fetch failed for:', article.url);
//               // Continue with original data
//             }
//           }

//           return {
//             id: `article-${Date.now()}-${index}`,
//             title: article.title || 'Untitled',
//             description: enrichedData.description || 'No description available',
//             source: article.source || 'Unknown Source',
//             publishedAt: article.published_date ? new Date(article.published_date) : new Date(),
//             imageUrl: enrichedData.imageUrl || 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800',
//             url: article.url || '#',
//           };
//         })
//       );

//       // Add AI response with news titles
//       const newsTitles = fetchedArticles.map((article) => ({
//         id: article.id,
//         title: article.title,
//       }));

//       const aiMessage: Message = {
//         id: `msg-${messageIdCounter.current++}`,
//         type: 'ai',
//         text: `Found ${fetchedArticles.length} articles about "${text}":`,
//         timestamp: new Date(),
//         newsTitles,
//       };
//       setMessages((prev) => [...prev, aiMessage]);

//       // Update articles in the right panel
//       setArticles(fetchedArticles);
//     } catch (error) {
//       console.error('Error fetching news:', error);

//       // Remove loading message
//       setMessages((prev) => prev.filter((msg) => msg.type !== 'loading'));

//       // Add error message
//       const errorMessage: Message = {
//         id: `msg-${messageIdCounter.current++}`,
//         type: 'ai',
//         text: 'Sorry, I encountered an error while fetching news. Please make sure the API server is running on localhost:8000.',
//         timestamp: new Date(),
//       };
//       setMessages((prev) => [...prev, errorMessage]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   return (
//     <div className="h-screen flex flex-col lg:flex-row overflow-hidden bg-gradient-to-br from-[#0f1419] via-[#14252a] to-[#1a3a3a]">
//       {/* Left Side - Chat Interface (40% on desktop, full width on mobile) */}
//       <div className="w-full lg:w-2/5 h-1/2 lg:h-full border-b lg:border-b-0 lg:border-r border-gray-700">
//         <ChatInterface
//           onSendMessage={handleSendMessage}
//           messages={messages}
//           onTitleClick={scrollToArticle}
//         />
//       </div>

//       {/* Right Side - News Preview (60% on desktop, full width on mobile) */}
//       <div className="w-full lg:w-3/5 h-1/2 lg:h-full">
//         <NewsPreview articles={articles} isLoading={isLoading} />
//       </div>
//     </div>
//   );
// }

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
    setMessages((prev) => [...prev, userMessage]);

    const loadingMessage: Message = {
      id: `msg-${messageIdCounter.current++}`,
      type: 'loading',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, loadingMessage]);
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

      setMessages((prev) => prev.filter((msg) => msg.type !== 'loading'));

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

      setMessages((prev) => [...prev, aiMessage]);

      // KEEP OLD ARTICLES + ADD NEW ONES
      setArticles((prev) => [...prev, ...fetchedArticles]);

    } catch (error) {
      console.error('Error fetching news:', error);
      setMessages((prev) => prev.filter((msg) => msg.type !== 'loading'));

      const errorMessage: Message = {
        id: `msg-${messageIdCounter.current++}`,
        type: 'ai',
        text: 'Sorry, I encountered an error while fetching news. Please make sure the API server is running on localhost:8000.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // return (
  //   <div className="h-screen flex bg-background text-foreground">
  //     <div className="w-full md:w-2/5 border-r border-gray-700">
  //       <ChatInterface
  //         onSendMessage={handleSendMessage}
  //         messages={messages}
  //         onTitleClick={scrollToArticle}
  //       />
  //     </div>
  //     <div className="hidden md:block md:w-3/5">
  //       <NewsPreview articles={articles} isLoading={isLoading} />
  //     </div>
  //   </div>
  // );
  return (
    <div className="flex flex-col lg:flex-row h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Left Side - Chat Interface (40% on desktop, full width on mobile) */}
      <div className="w-full lg:w-2/5 border-r border-gray-700 flex flex-col h-full lg:h-full">
        <ChatInterface
          messages={messages}
          onSendMessage={handleSendMessage}
          onTitleClick={scrollToArticle}
        />
      </div>
      {/* Right Side - News Preview (60% on desktop, hidden on mobile) */}
      <div className="hidden lg:block lg:w-3/5 overflow-y-auto h-full">
        <NewsPreview articles={articles} />
      </div>
    </div>
  );

}

export default Index;