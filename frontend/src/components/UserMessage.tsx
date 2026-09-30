interface UserMessageProps {
  text: string;
  timestamp: Date;
}

export function UserMessage({ text, timestamp }: UserMessageProps) {
  return (
    <div className="flex justify-end items-start gap-3 animate-slide-in">
      <div className="flex flex-col items-end max-w-[80%]">
        <div className="bg-gradient-to-br from-cyan-500 to-cyan-700 rounded-2xl rounded-tr-sm px-4 py-3 shadow-[0_4px_12px_hsl(190_100%_50%/0.3)]">
          <p className="text-sm text-primary-foreground font-medium">{text}</p>
        </div>
        <p className="text-xs text-muted-foreground mt-1.5 mr-1">
          {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </div>
  );
}