import type { MessageProps } from "../types"
import { Bot, User } from "lucide-react"
import { cn } from "@/lib/utils"

export function ChatMessage({ message }: MessageProps) {
  return (
    <div
      className={cn(
        "flex w-full items-start gap-4 rounded-lg p-4",
        message.role === "user" ? "bg-muted/50" : "bg-background",
      )}
    >
      <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border bg-background shadow">
        {message.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>
      <div className="flex-1 space-y-2">
        <p className="text-sm text-muted-foreground">{message.role === "user" ? "You" : "AI Assistant"}</p>
        <div className="space-y-4">
          <p className="text-sm">{message.content}</p>
        </div>
      </div>
    </div>
  )
}

