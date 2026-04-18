import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Activity } from 'lucide-react';
import './index.css';

interface Message {
  id: string;
  role: 'user' | 'system';
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init',
      role: 'system',
      content: 'Welcome to the PubMed AI Research Assistant. Enter your medical inquiry below.'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: input.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage.content })
      });
      
      if (!response.ok) throw new Error('API request failed');
      const data = await response.json();
      
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: data.answer
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'system',
        content: "Error: Could not connect to the PubMed RAG backend. Please ensure the API is running on port 8000."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <Activity color="var(--accent-light)" size={28} />
        <div>
          <h1>PubMed Chatbot</h1>
          <p>AI-Powered Medical Research Assistant</p>
        </div>
      </div>

      <div className="chat-area" ref={scrollRef}>
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="message-label">
              {msg.role === 'system' ? <Bot size={14} /> : <User size={14} />}
              {msg.role === 'system' ? 'System' : 'You'}
            </div>
            <div className="message-bubble">
               {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message system">
             <div className="message-label">
              <Bot size={14} />
              System
            </div>
            <div className="message-bubble">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="input-area">
        <form onSubmit={handleSubmit} className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about medical research..."
            disabled={isLoading}
          />
          <button type="submit" className="send-btn" disabled={!input.trim() || isLoading}>
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
