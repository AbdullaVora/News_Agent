import { NewsCard } from './NewsCard';
import { Newspaper } from 'lucide-react';

interface NewsArticle {
  id: string;
  title: string;
  description: string;
  source: string;
  publishedAt: Date;
  imageUrl: string;
  url: string;
}

interface NewsPreviewProps {
  articles: NewsArticle[];
  isLoading?: boolean;
}

// export function NewsPreview({ articles, isLoading }: NewsPreviewProps) {
//   if (isLoading) {
//     return (
//       <div className="h-full flex items-center justify-center bg-transparent">
//         <div className="text-center">
//           <div className="inline-block p-4 rounded-full bg-transparent mb-4 animate-pulse shadow-glow border border-primary/20">
//             <Newspaper className="w-12 h-12 text-primary" />
//           </div>
//           <p className="text-sm text-muted-foreground">Loading articles...</p>
//         </div>
//       </div>
//     );
//   }

//   if (articles.length === 0) {
//     return (
//       <div className="h-full flex items-center justify-center bg-transparent">
//         <div className="text-center max-w-md px-6">
//           <div className="inline-block p-4 rounded-full bg-transparent mb-4 shadow-glow border border-primary/20">
//             <Newspaper className="w-12 h-12 text-primary" />
//           </div>
//           <h3 className="text-xl font-bold mb-2 text-foreground">No News Yet</h3>
//           <p className="text-sm text-muted-foreground">
//             Enter a search query in the chat to discover the latest news articles
//           </p>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="h-full overflow-y-auto bg-transparent">
//       <div className="p-6">
//         <div className="mb-6">
//           <h2 className="text-2xl font-bold mb-1 text-foreground">Latest Articles</h2>
//           <p className="text-sm text-muted-foreground">
//             {articles.length} {articles.length === 1 ? 'article' : 'articles'} found
//           </p>
//         </div>
//         <div className="grid gap-6">
//           {articles.map((article, index) => (
//             <NewsCard
//               key={article.id}
//               article={article}
//               index={index}
//             />
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// }

export function NewsPreview({ articles, isLoading }: { articles: NewsArticle[]; isLoading?: boolean }) {
  if (isLoading && articles.length === 0) {
    return (
      <div className="h-full flex items-center justify-center bg-transparent">
        <div className="text-center">
          <div className="inline-block p-4 rounded-full bg-transparent mb-4 animate-pulse shadow-glow border border-primary/20">
            <Newspaper className="w-12 h-12 text-primary" />
          </div>
          <p className="text-sm text-muted-foreground">Loading articles...</p>
        </div>
      </div>
    );
  }

  if (articles.length === 0) {
    return (
      <div className="h-full flex items-center justify-center bg-transparent">
        <div className="text-center max-w-md px-6">
          <div className="inline-block p-4 rounded-full bg-transparent mb-4 shadow-glow border border-primary/20">
            <Newspaper className="w-12 h-12 text-primary" />
          </div>
          <h3 className="text-xl font-bold mb-2 text-foreground">No News Yet</h3>
          <p className="text-sm text-muted-foreground">
            Enter a search query in the chat to discover the latest news articles
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto bg-transparent">
      <div className="p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold mb-1 text-foreground">Latest Articles</h2>
          <p className="text-sm text-muted-foreground">
            {articles.length} {articles.length === 1 ? 'article' : 'articles'} found
          </p>
        </div>
        <div className="grid gap-6">
          {articles.map((article, index) => (
            <NewsCard
              key={article.id}
              article={article}
              index={index}
            />
          ))}
        </div>
      </div>
    </div>
  );
}