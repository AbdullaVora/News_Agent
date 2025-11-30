import { Sparkles, Search, Brain, Zap } from 'lucide-react';
import React, { useState, useEffect } from 'react';

// export function AIMessage({
//   text,
//   timestamp,
//   isLoading,
//   newsTitles,
//   onTitleClick
// }: {
//   text?: string;
//   timestamp?: Date;
//   isLoading?: boolean;
//   newsTitles?: Array<{ id: string; title: string }>;
//   onTitleClick?: (id: string) => void;
// }) {
//   if (isLoading) {
//     return (
//       <div className="flex items-start gap-3 animate-slide-in">
//         <div className="p-2.5 rounded-lg bg-gradient-to-br from-cyan/20 to-cyan-light/10 border border-cyan/30 shadow-[0_0_20px_hsl(190_100%_50%/0.15)]">
//           <Sparkles className="w-4 h-4 text-cyan animate-pulse" />
//         </div>
//         <div className="flex-1 max-w-[80%]">
//           <div className="bg-gradient-to-br from-card to-muted/50 backdrop-blur-sm border border-border/50 rounded-2xl rounded-tl-sm px-4 py-3 shadow-[0_2px_8px_hsl(0_0%_0%/0.3)]">
//             <div className="flex items-center gap-1.5">
//               <div className="flex gap-1">
//                 <div className="w-2 h-2 bg-cyan/60 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
//                 <div className="w-2 h-2 bg-cyan/60 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
//                 <div className="w-2 h-2 bg-cyan/60 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
//               </div>
//               <p className="text-xs text-muted-foreground ml-1">searching...</p>
//             </div>
//           </div>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="flex items-start gap-3 animate-slide-in">
//       <div className="p-2.5 rounded-lg bg-gradient-to-br from-cyan/20 to-cyan-light/10 border border-cyan/30 shadow-[0_0_20px_hsl(190_100%_50%/0.15)]">
//         <Sparkles className="w-4 h-4 text-cyan" />
//       </div>
//       <div className="flex-1 max-w-[80%]">
//         <div className="bg-gradient-to-br from-card to-muted/50 backdrop-blur-sm border border-border/50 rounded-2xl rounded-tl-sm px-4 py-3 shadow-[0_2px_8px_hsl(0_0%_0%/0.3)]">
//           {text && <p className="text-sm text-foreground/90 mb-2">{text}</p>}
//           {newsTitles && newsTitles.length > 0 && (
//             <ul className="space-y-1.5 mt-2">
//               {newsTitles.map((item) => (
//                 <li key={item.id}>
//                   <button
//                     onClick={() => onTitleClick?.(item.id)}
//                     className="text-sm text-cyan hover:text-cyan-light transition-colors text-left w-full flex items-start gap-2 group"
//                   >
//                     <span className="text-cyan/60 group-hover:text-cyan transition-colors">•</span>
//                     <span className="flex-1 underline decoration-cyan/30 hover:decoration-cyan/60 underline-offset-2">
//                       {item.title}
//                     </span>
//                   </button>
//                 </li>
//               ))}
//             </ul>
//           )}
//         </div>
//         {timestamp && (
//           <p className="text-xs text-muted-foreground mt-1.5 ml-1">
//             {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
//           </p>
//         )}
//       </div>
//     </div>
//   );
// }


export function AIMessage({
  text,
  timestamp,
  isLoading,
  newsTitles,
  onTitleClick
}: {
  text?: string;
  timestamp?: Date;
  isLoading?: boolean;
  newsTitles?: Array<{ id: string; title: string }>;
  onTitleClick?: (id: string) => void;
}) {
  const [loadingPhase, setLoadingPhase] = useState(0);
  const loadingMessages = [
    'Searching...',
    'Analyzing results...',
    'Processing information...',
    'Generating response...'
  ];

  useEffect(() => {
    if (isLoading) {
      const interval = setInterval(() => {
        setLoadingPhase((prev) => (prev + 1) % loadingMessages.length);
      }, 2000);
      return () => clearInterval(interval);
    } else {
      setLoadingPhase(0);
    }
  }, [isLoading]);

  if (isLoading) {
    return (
      <div className="flex items-start gap-3 animate-slide-in">
        <div className="p-2.5 rounded-lg bg-gradient-to-br from-cyan-500/20 to-cyan-300/10 border border-cyan-500/30 shadow-[0_0_20px_rgba(6,182,212,0.15)] animate-pulse-glow">
          <Sparkles className="w-4 h-4 text-cyan-400 animate-spin-slow" />
        </div>
        <div className="flex-1 max-w-[80%]">
          <div className="bg-gradient-to-br from-slate-800 to-slate-700/50 backdrop-blur-sm border border-slate-600/50 rounded-2xl rounded-tl-sm px-4 py-3 shadow-[0_2px_8px_rgba(0,0,0,0.3)]">
            {/* Animated dots */}
            <div className="flex items-center gap-2 mb-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-cyan-400/60 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-cyan-400/60 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-cyan-400/60 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
              <p className="text-xs text-slate-400 transition-all duration-500">
                {loadingMessages[loadingPhase]}
              </p>
            </div>

            {/* Simulated typing lines */}
            <div className="space-y-2">
              <div className="h-2 bg-gradient-to-r from-cyan-500/30 to-transparent rounded animate-pulse-width" />
              <div className="h-2 bg-gradient-to-r from-cyan-500/30 to-transparent rounded animate-pulse-width w-4/5" style={{ animationDelay: '0.2s' }} />
              <div className="h-2 bg-gradient-to-r from-cyan-500/30 to-transparent rounded animate-pulse-width w-3/5" style={{ animationDelay: '0.4s' }} />
            </div>

            {/* Processing indicator */}
            <div className="flex items-center gap-2 mt-3 text-xs text-cyan-400/70">
              <Brain className="w-3 h-3 animate-pulse" />
              <span>AI thinking...</span>
              <Zap className="w-3 h-3 animate-pulse" style={{ animationDelay: '0.5s' }} />
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-3 animate-slide-in">
      <div className="p-2.5 rounded-lg bg-gradient-to-br from-cyan-500/20 to-cyan-300/10 border border-cyan-500/30 shadow-[0_0_20px_rgba(6,182,212,0.15)]">
        <Sparkles className="w-4 h-4 text-cyan-400" />
      </div>
      <div className="flex-1 max-w-[80%]">
        <div className="bg-gradient-to-br from-slate-800 to-slate-700/50 backdrop-blur-sm border border-slate-600/50 rounded-2xl rounded-tl-sm px-4 py-3 shadow-[0_2px_8px_rgba(0,0,0,0.3)]">
          {text && <p className="text-sm text-slate-100 mb-2">{text}</p>}
          {newsTitles && newsTitles.length > 0 && (
            <ul className="space-y-1.5 mt-2">
              {newsTitles.map((item) => (
                <li key={item.id}>
                  <button
                    onClick={() => onTitleClick?.(item.id)}
                    className="text-sm text-cyan-400 hover:text-cyan-300 transition-colors text-left w-full flex items-start gap-2 group"
                  >
                    <span className="text-cyan-400/60 group-hover:text-cyan-400 transition-colors">•</span>
                    <span className="flex-1 underline decoration-cyan-400/30 hover:decoration-cyan-400/60 underline-offset-2">
                      {item.title}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
        {timestamp && (
          <p className="text-xs text-slate-500 mt-1.5 ml-1">
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        )}
      </div>
    </div>
  );
}

// Demo component to showcase the loading states
export default function AILoadingDemo() {
  const [isLoading, setIsLoading] = useState(true);
  const [showResult, setShowResult] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
      setShowResult(true);
    }, 8000);
    return () => clearTimeout(timer);
  }, []);

  const handleRestart = () => {
    setIsLoading(true);
    setShowResult(false);
    setTimeout(() => {
      setIsLoading(false);
      setShowResult(true);
    }, 8000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <style>{`
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes pulse-glow {
          0%, 100% { box-shadow: 0 0 20px rgba(6,182,212,0.15); }
          50% { box-shadow: 0 0 30px rgba(6,182,212,0.3); }
        }
        @keyframes pulse-width {
          0%, 100% { width: 0%; opacity: 0.3; }
          50% { width: 100%; opacity: 0.6; }
        }
        @keyframes slide-in {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-spin-slow {
          animation: spin-slow 3s linear infinite;
        }
        .animate-pulse-glow {
          animation: pulse-glow 2s ease-in-out infinite;
        }
        .animate-pulse-width {
          animation: pulse-width 1.5s ease-in-out infinite;
        }
        .animate-slide-in {
          animation: slide-in 0.3s ease-out;
        }
      `}</style>

      <div className="max-w-3xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-white mb-2">AI Loading States</h1>
          <p className="text-slate-400">Watch the AI thinking process</p>
        </div>

        <div className="space-y-4">
          {isLoading && <AIMessage isLoading={true} />}
          
          {showResult && (
            <AIMessage
              text="Here are the latest news articles I found for you:"
              timestamp={new Date()}
              newsTitles={[
                { id: '1', title: 'Breaking: Major AI breakthrough announced' },
                { id: '2', title: 'Tech industry sees rapid growth in Q4' },
                { id: '3', title: 'New sustainability initiatives launched globally' }
              ]}
              onTitleClick={(id) => alert(`Clicked article: ${id}`)}
            />
          )}
        </div>

        <div className="mt-8 text-center">
          <button
            onClick={handleRestart}
            className="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition-colors shadow-lg shadow-cyan-500/30"
          >
            Restart Demo
          </button>
        </div>
      </div>
    </div>
  );
}
