import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Sparkles, Send, Newspaper, TrendingUp } from 'lucide-react';
import { UserMessage } from './UserMessage';
import { AIMessage } from './AIMessage';

interface Message {
  id: string;
  type: 'user' | 'ai' | 'loading';
  text?: string;
  timestamp: Date;
  newsTitles?: Array<{ id: string; title: string }>;
}

interface ChatInterfaceProps {
  onSendMessage: (message: string) => void;
  messages: Message[];
  onTitleClick?: (id: string) => void;
}

export function ChatInterface({ onSendMessage, messages, onTitleClick }: ChatInterfaceProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const quickActions = [
    { label: 'Latest Tech News', icon: Newspaper },
    { label: 'Trending Stories', icon: TrendingUp },
  ];

  return (
    <div className="h-full flex flex-col bg-transparent">
      {/* Header */}
      <div className="p-6 border-b border-gray-700 bg-card/20 backdrop-blur-sm">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 rounded-lg bg-gradient-to-br from-primary to-primary-light shadow-glow">
            <Sparkles className="w-5 h-5 text-primary-foreground" />
          </div>
          <div>
            <h2 className="text-xl font-bold bg-gradient-to-r from-primary to-primary-light bg-clip-text text-transparent">
              News Aggregator AI
            </h2>
            <p className="text-sm text-muted-foreground">
              Ask me to find the latest news articles
            </p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="p-4 rounded-full bg-gradient-to-br from-primary/10 to-primary-light/10 mb-4 shadow-glow">
              <Newspaper className="w-12 h-12 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2 text-foreground">Start Your Search</h3>
            <p className="text-sm text-muted-foreground max-w-xs">
              Enter a topic or keyword to discover the latest news articles
            </p>
          </div>
        ) : (
          messages.map((message) => {
            if (message.type === 'user') {
              return <UserMessage key={message.id} text={message.text || ''} timestamp={message.timestamp} />;
            } else if (message.type === 'loading') {
              return <AIMessage key={message.id} isLoading={true} />;
            } else {
              return (
                <AIMessage
                  key={message.id}
                  text={message.text}
                  timestamp={message.timestamp}
                  newsTitles={message.newsTitles}
                  onTitleClick={onTitleClick}
                />
              );
            }
          })
        )}
      </div>

      {/* Quick Actions */}
      {messages.length === 0 && (
        <div className="px-6 pb-4">
          <div className="flex gap-2">
            {quickActions.map((action) => (
              <Button
                key={action.label}
                variant="outline"
                size="sm"
                onClick={() => onSendMessage(action.label)}
                className="flex-1 gap-2 hover:bg-primary/5 hover:border-primary/50 transition-all border-gray-700"
              >
                <action.icon className="w-4 h-4" />
                <span className="text-xs">{action.label}</span>
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="p-6 border-t border-gray-700 bg-card/20 backdrop-blur-sm">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Search for news..."
            className="flex-1 bg-background/80 border-gray-700 focus:border-primary/70 focus:ring-2 focus:ring-primary/30 transition-all shadow-[0_0_20px_hsl(190_100%_50%/0.1)] focus:shadow-[0_0_30px_hsl(190_100%_50%/0.2)]"
          />
          <Button
            type="submit"
            size="icon"
            disabled={!inputValue.trim()}
            className="bg-gradient-to-br from-primary to-primary-light hover:shadow-glow transition-all"
          >
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </div>
    </div>
  );
}