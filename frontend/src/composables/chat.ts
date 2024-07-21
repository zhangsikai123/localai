interface Message {
  id: number;
  sender: string;
  content: string;
  thread_id: number;
  created_at: string;
}

interface ParsedMessage {
  role: string;
  content: string;
}

export function parseHistory(input: any[], history_window: int): ParsedMessage[] {
  const messages: ParsedMessage[] = [];
  // Iterate over each message object in the input array from the end to the beginning
  for (const message of input.slice(-history_window).reverse()) {
    const { sender, content } = message;
    const role = sender === 'user' ? 'user' : 'assistant';
    messages.push({ role, content });
  }
  messages.reverse();
  return messages;
}
