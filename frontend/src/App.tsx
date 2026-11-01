import { useEffect, useRef, useState } from 'react'
import { checkHealth, sendMessage } from './api'
import './App.css'

interface Message {
  role: 'user' | 'assistant'
  text: string
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isSending, setIsSending] = useState(false)
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    checkHealth()
      .then(() => setApiStatus('online'))
      .catch(() => setApiStatus('offline'))
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend() {
    const text = input.trim()
    if (!text || isSending) return

    setMessages((prev) => [...prev, { role: 'user', text }])
    setInput('')
    setIsSending(true)

    try {
      const reply = await sendMessage(text, sessionId)
      setSessionId(reply.session_id)
      setMessages((prev) => [...prev, { role: 'assistant', text: reply.response }])
    } catch (err) {
      const detail = err instanceof Error ? err.message : String(err)
      setMessages((prev) => [...prev, { role: 'assistant', text: `Error: ${detail}` }])
    } finally {
      setIsSending(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') handleSend()
  }

  return (
    <div className="chat-app">
      <header className="chat-header">
        <h1>Claude Weather Agent</h1>
        <span className={`status status-${apiStatus}`}>API: {apiStatus}</span>
      </header>

      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble chat-bubble-${m.role}`}>
            {m.text}
          </div>
        ))}
        {isSending && <div className="chat-bubble chat-bubble-assistant">Thinking...</div>}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-row">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about the weather..."
          disabled={isSending}
        />
        <button onClick={handleSend} disabled={isSending || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}

export default App
