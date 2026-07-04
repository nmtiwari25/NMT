import { useState } from "react";

export default function App() {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hi! Type 'hi', 'help', 'about', or 'bye' to try me out." },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);

  async function sendMessage(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending) return;

    setMessages((prev) => [...prev, { from: "user", text }]);
    setInput("");
    setSending(true);

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { from: "bot", text: data.reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { from: "bot", text: "Error reaching the backend. Is app.py running on port 5000?" },
      ]);
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="chat-container">
      <h1>NMT WhatsApp Bot (Preview)</h1>
      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.from}`}>
            {m.text}
          </div>
        ))}
      </div>
      <form className="chat-input" onSubmit={sendMessage}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={sending}
        />
        <button type="submit" disabled={sending}>
          Send
        </button>
      </form>
    </div>
  );
}
