import { Sparkles } from 'lucide-react';

interface AIMessageProps {
  text?: string;
  timestamp?: Date;
  isLoading?: boolean;
  newsTitles?: Array<{ id: string; title: string }>;
  onTitleClick?: (id: string) => void;
}

export function AIMessage({ text, timestamp, isLoading, newsTitles, onTitleClick }: AIMessageProps) {
  if (isLoading) {
    return (
      <div className="flex items-start gap-3 animate-slide-in">
        <div className="p-2.5 rounded-lg bg-gradient-to-br from-cyan/20 to-cyan-light/10 border border-cyan/30 shadow-[0_0_20px_hsl(190_100%_50%/0.15)]">
          <Sparkles className="w-4 h-4 text-cyan animate-pulse" />
        </div>
        <div className="flex-1 max-w-[80%]">
          <div className="bg-gradient-to-br from-card to-muted/50 backdrop-blur-sm border border-border/50 rounded-2xl rounded-tl-sm px-4 py-3 shadow-[0_2px_8px_hsl(0_0%_0%/0.3)]">
            <div className="flex items-center gap-1.5">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-cyan/60 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-cyan/60 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-cyan/60 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
              <p className="text-xs text-muted-foreground ml-1">searching...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-3 animate-slide-in">
      <div className="p-2.5 rounded-lg bg-gradient-to-br from-cyan/20 to-cyan-light/10 border border-cyan/30 shadow-[0_0_20px_hsl(190_100%_50%/0.15)]">
        <Sparkles className="w-4 h-4 text-cyan" />
      </div>
      <div className="flex-1 max-w-[80%]">
        <div className="bg-gradient-to-br from-card to-muted/50 backdrop-blur-sm border border-border/50 rounded-2xl rounded-tl-sm px-4 py-3 shadow-[0_2px_8px_hsl(0_0%_0%/0.3)]">
          {text && <p className="text-sm text-foreground/90 mb-2">{text}</p>}
          {newsTitles && newsTitles.length > 0 && (
            <ul className="space-y-1.5 mt-2">
              {newsTitles.map((item) => (
                <li key={item.id}>
                  <button
                    onClick={() => onTitleClick?.(item.id)}
                    className="text-sm text-cyan hover:text-cyan-light transition-colors text-left w-full flex items-start gap-2 group"
                  >
                    <span className="text-cyan/60 group-hover:text-cyan transition-colors">•</span>
                    <span className="flex-1 underline decoration-cyan/30 hover:decoration-cyan/60 underline-offset-2">
                      {item.title}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
        {timestamp && (
          <p className="text-xs text-muted-foreground mt-1.5 ml-1">
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </p>
        )}
      </div>
    </div>
  );
}