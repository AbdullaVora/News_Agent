import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ExternalLink, Clock, Newspaper } from 'lucide-react';

interface NewsArticle {
  id: string;
  title: string;
  description: string;
  source: string;
  publishedAt: Date;
  imageUrl?: string;
  generated_image?: string;
  url: string;
}

interface NewsCardProps {
  article: NewsArticle;
  index: number;
}

// export function NewsCard({ article, index }: NewsCardProps) {
//   const [imageError, setImageError] = useState(false);
//   const [isExpanded, setIsExpanded] = useState(false);

//   // Format relative time
//   const formatTimeAgo = (date: Date) => {
//     const now = new Date();
//     const diffMs = now.getTime() - date.getTime();
//     const diffMins = Math.floor(diffMs / (1000 * 60));
//     const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
//     const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

//     if (diffMins < 1) return 'just now';
//     if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
//     if (diffHrs < 24) return `${diffHrs} hour${diffHrs > 1 ? 's' : ''} ago`;
//     if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

//     return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
//   };

//   // Check if description is long (more than 150 characters)
//   const isLongDescription = article.description.length > 150;
//   const displayDescription = isExpanded
//     ? article.description
//     : article.description.slice(0, 150) + (isLongDescription ? '...' : '');

//   return (
//     <Card
//       id={`article-${article.id}`}
//       className="group overflow-hidden border-border/50 bg-card/60 backdrop-blur-sm hover:shadow-[0_10px_30px_-10px_hsl(190_100%_50%/0.4)] hover:border-primary/50 transition-all duration-300 animate-slide-in scroll-mt-6"
//       style={{ animationDelay: `${index * 100}ms` }}
//     >
//       <div className="aspect-video relative overflow-hidden bg-muted">
//         {!imageError ? (
//           <img
//             src={article.imageUrl || article.generated_image}
//             alt={article.title}
//             className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
//             onError={() => setImageError(true)}
//             loading="lazy"
//           />
//         ) : (
//           <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
//             <Newspaper className="w-16 h-16 text-gray-600" />
//           </div>
//         )}
//         <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-60 group-hover:opacity-40 transition-opacity duration-300" />
//       </div>

//       <CardHeader className="pb-3">
//         <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
//           <span className="px-2 py-1 rounded-md bg-primary/15 text-primary font-medium border border-primary/20">
//             {article.source}
//           </span>
//           <span className="flex items-center gap-1">
//             <Clock className="w-3 h-3" />
//             {formatTimeAgo(article.publishedAt)}
//           </span>
//         </div>
//         <CardTitle className="line-clamp-2 group-hover:text-primary transition-colors">
//           {article.title}
//         </CardTitle>
//       </CardHeader>

//       <CardContent className="pb-4">
//         <CardDescription className="text-muted-foreground whitespace-pre-line">
//           {displayDescription}
//         </CardDescription>

//         {isLongDescription && (
//           <button
//             onClick={() => setIsExpanded(!isExpanded)}
//             className="text-sm text-primary hover:text-primary/80 transition-colors mt-2 font-medium"
//           >
//             {isExpanded ? '← Show less' : 'Read more →'}
//           </button>
//         )}
//       </CardContent>

//       <CardFooter>
//         <Button
//           variant="outline"
//           size="sm"
//           className="w-full gap-2 hover:bg-primary/15 hover:border-primary/60 hover:text-primary transition-all border-border/50 hover:shadow-[0_0_15px_hsl(190_100%_50%/0.2)]"
//           onClick={() => window.open(article.url, '_blank')}
//         >
//           Read Article
//           <ExternalLink className="w-4 h-4" />
//         </Button>
//       </CardFooter>
//     </Card>
//   );
// }

export function NewsCard({ article, index }: { article: NewsArticle; index: number }) {
  const [imageError, setImageError] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const formatTimeAgo = (date: Date) => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHrs < 24) return `${diffHrs} hour${diffHrs > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const isLongDescription = article.description.length > 150;
  const displayDescription = isExpanded
    ? article.description
    : article.description.slice(0, 150) + (isLongDescription ? '...' : '');

  return (
    <Card
      id={`article-${article.id}`}
      className="group overflow-hidden border-border/50 bg-card/60 backdrop-blur-sm hover:shadow-[0_10px_30px_-10px_hsl(190_100%_50%/0.4)] hover:border-primary/50 transition-all duration-300 animate-slide-in scroll-mt-6"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      <div className="aspect-video relative overflow-hidden bg-muted">
        {!imageError ? (
          <img
            src={article.imageUrl || article.generated_image}
            alt={article.title}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
            onError={() => setImageError(true)}
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
            <Newspaper className="w-16 h-16 text-gray-600" />
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-60 group-hover:opacity-40 transition-opacity duration-300" />
      </div>

      <CardHeader className="pb-3">
        <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
          <span className="px-2 py-1 rounded-md bg-primary/15 text-primary font-medium border border-primary/20">
            {article.source}
          </span>
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {formatTimeAgo(article.publishedAt)}
          </span>
        </div>
        <CardTitle className="line-clamp-2 group-hover:text-primary transition-colors">
          {article.title}
        </CardTitle>
      </CardHeader>

      <CardContent className="pb-4">
        <CardDescription className="text-muted-foreground whitespace-pre-line">
          {displayDescription}
        </CardDescription>

        {isLongDescription && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-sm text-primary hover:text-primary/80 transition-colors mt-2 font-medium"
          >
            {isExpanded ? '← Show less' : 'Read more →'}
          </button>
        )}
      </CardContent>

      <CardFooter>
        <Button
          variant="outline"
          size="sm"
          className="w-full gap-2 hover:bg-primary/15 hover:border-primary/60 hover:text-primary transition-all border-border/50 hover:shadow-[0_0_15px_hsl(190_100%_50%/0.2)]"
          onClick={() => window.open(article.url, '_blank')}
        >
          Read Article
          <ExternalLink className="w-4 h-4" />
        </Button>
      </CardFooter>
    </Card>
  );
}