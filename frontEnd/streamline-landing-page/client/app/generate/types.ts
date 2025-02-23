export type Message = {
  id: string
  role: "user" | "assistant"
  content: string
}

export type MessageProps = {
  message: Message
}

