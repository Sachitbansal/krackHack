"use client"
import { useRef, useEffect } from "react";
import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { ArrowRight, SendHorizontal, Wand2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ChatMessage } from "./components/chat-message"
import type { Message } from "./types"
import { ScrollArea } from "@/components/ui/scroll-area"
import { json } from "stream/consumers";

// Replace this with your actual API endpoint
const API_URL = "http://127.0.0.1:5000/editProject"
let username = "username"
let projectname = "projectname"
export default function GeneratePage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [projectDetails, setProjectDetails] = useState({})
  const [input, setInput] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)

  const addMessage = (content: string, role: "user" | "assistant") => {
    const newMessage: Message = {
      id: Math.random().toString(36).substring(7),
      content,
      role,
    }
    setMessages((prev) => [...prev, newMessage])
  }

  const fetchAIResponse = async (message: string) => {
    setIsGenerating(true);
  
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: message }), // Send user input to Flask
      });
  
      const data = await response.json();
  
      // Assuming API returns { output: "AI response" }
      if (data.msg) {
        addMessage(data.msg, "assistant");
      } else {
        addMessage("Error getting response from AI.", "assistant");
      }
    } catch (error) {
      addMessage("Failed to connect to AI server.", "assistant");
    }
  
    setIsGenerating(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isGenerating) return

    addMessage(input, "user")
    setInput("")
    await fetchAIResponse(input)
  }
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {  // Prevents newline if Shift is not pressed
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

useEffect(() => {
  const fetchProj = async ()=>{
    const data: string | null = localStorage.getItem('projectDetails');
    const parsedData: string = data ? JSON.parse(data) : '';
    setProjectDetails(parsedData);
    console.log(parsedData)
}

  fetchProj();
  
  messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
}, [messages]);  // Scrolls when messages update

  return (
    <div className="container max-w-screen-xl py-12">
      <div className="mx-auto max-w-4xl space-y-8">
        <div className="space-y-4 text-center">
          <h1 className="bg-gradient-to-br from-foreground from-30% via-foreground/90 to-foreground/70 bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-5xl">
            Make Changes To Your Website
          </h1>
          <h4 className="text-muted-foreground text-1xl">
            Describe what all changes you want to make to your website.
          </h4>
          <h4 className="text-muted-foreground text-1xl">
            Your current website is hosted at : <a href="http://github.com/psudeoR3BEL/complexProject"> http://github.com/psudeoR3BEL/complexProject</a>
          </h4>
        </div>

        <Card className="border-2 border-border/50 bg-background/50 backdrop-blur">
          <CardHeader>
        
          </CardHeader>
          <CardContent className="p-6 space-y-4">
          <ScrollArea className="h-[300px] pr-4">
  {messages.length === 0 ? (
    <div className="flex flex-col items-center justify-center h-full space-y-4 text-center text-muted-foreground">
      <Wand2 className="h-12 w-12" />
      <p>What would you like us to change?</p>
    </div>
  ) : (
    <div className="space-y-4">
      {messages.map((message) => (
        <ChatMessage key={message.id} message={message} />
      ))}
      {isGenerating && (
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <div className="animate-spin">◌</div>
          AI is typing...
        </div>
      )}
      <div ref={messagesEndRef} />  {/* Dummy div for auto-scroll */}
    </div>
  )}
</ScrollArea>

            <form onSubmit={handleSubmit} className="flex gap-4">
            <Textarea
  placeholder="Enter the changes here..."
  className="min-h-[80px] resize-none border-border/50 bg-background/50 backdrop-blur"
  value={input}
  onChange={(e) => setInput(e.target.value)}
  onKeyDown={handleKeyDown}  // Add this event
/>
              <Button type="submit" size="icon" disabled={!input.trim() || isGenerating}>
                <SendHorizontal className="h-4 w-4" />
                <span className="sr-only">Send message</span>
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}