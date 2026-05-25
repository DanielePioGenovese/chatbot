import { BotMessageSquare, CircleGauge, Microscope, Send, Truck, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "http://localhost:9998/agent";

const services = [
  {
    icon: CircleGauge,
    title: "Turned Small Parts",
    text: "Custom production of precision metallic micro-components with millesimal tolerances.",
  },
  {
    icon: Microscope,
    title: "Quality Inspection",
    text: "Advanced laser-vision telemetry systems ensuring absolute zero-defect batch metrics.",
  },
  {
    icon: Truck,
    title: "Express Logistics",
    text: "Guaranteed 24/48h delivery execution corridors across Europe for all stock lines.",
  },
];

async function fetchAgentResponse(userPrompt) {
  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ prompt: userPrompt }),
    });

    if (!response.ok) {
      throw new Error(`Server returned unexpected error state: ${response.status}`);
    }

    const data = await response.json();
    return data.answer;
  } catch (error) {
    console.error("Critical failure during API retrieval loop:", error);
    return "Connection error";
  }
}

function ChatBubble({ text, isUser }) {
  return (
    <div className={`message-row ${isUser ? "message-row-user" : ""}`}>
      <div className={`message-bubble ${isUser ? "message-bubble-user" : "message-bubble-agent"}`}>
        {text}
      </div>
    </div>
  );
}

function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      text: "Welcome! I am the TechLogic AI assistant. How can I help you today?",
      isUser: false,
    },
  ]);
  const inputRef = useRef(null);
  const messagesRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  async function handleSubmit(event) {
    event.preventDefault();

    const messageText = inputValue.trim();
    if (!messageText || isLoading) return;

    setInputValue("");
    setMessages((currentMessages) => [
      ...currentMessages,
      { id: crypto.randomUUID(), text: messageText, isUser: true },
    ]);
    setIsLoading(true);

    const agentReply = await fetchAgentResponse(messageText);

    setIsLoading(false);
    setMessages((currentMessages) => [
      ...currentMessages,
      { id: crypto.randomUUID(), text: agentReply, isUser: false },
    ]);
  }

  return (
    <>
      <button className="chat-toggle" type="button" onClick={() => setIsOpen((current) => !current)}>
        <BotMessageSquare size={24} />
        <span>Chat Support</span>
      </button>

      {isOpen && (
        <aside className="chat-window" aria-label="TechLogic AI chat">
          <div className="chat-header">
            <div className="chat-brand">
              <div className="chat-logo">TL</div>
              <div>
                <h3>AI Assistant | TechLogic</h3>
                <div className="chat-status">
                  <span />
                  Online & Connected
                </div>
              </div>
            </div>
            <button className="chat-close" type="button" aria-label="Close chat" onClick={() => setIsOpen(false)}>
              <X size={20} />
            </button>
          </div>

          <div className="chat-messages" ref={messagesRef}>
            {messages.map((message) => (
              <ChatBubble key={message.id} text={message.text} isUser={message.isUser} />
            ))}
          </div>

          {isLoading && (
            <div className="chat-loading">
              <span className="spinner" />
              <span>[Retrieval & Agent Inference in progress]...</span>
            </div>
          )}

          <form className="chat-form" onSubmit={handleSubmit}>
            <input
              ref={inputRef}
              type="text"
              placeholder="Type your question here..."
              autoComplete="off"
              value={inputValue}
              onChange={(event) => setInputValue(event.target.value)}
            />
            <button type="submit" aria-label="Send message" disabled={isLoading}>
              <Send size={20} />
            </button>
          </form>
        </aside>
      )}
    </>
  );
}

function App() {
  return (
    <main>
      <nav className="site-nav">
        <div className="brand">
          TECH<span>LOGIC</span>
        </div>
        <div className="nav-links">
          <a href="#services">Products</a>
          <a href="#services">Quality Control</a>
          <a href="#company">Company</a>
          <a href="#contact">Contact Us</a>
        </div>
        <a className="quote-button" href="#contact">
          Get a Quote
        </a>
      </nav>

      <header className="hero">
        <div className="hero-content">
          <h1>Precision in Every Detail</h1>
          <p>
            High-quality mechanical components for modern industry. 24/7 technical support powered by
            our virtual AI assistant.
          </p>
          <a href="#services" className="hero-button">
            Explore Products
          </a>
        </div>
      </header>

      <section id="services" className="services-section">
        <h2>Our Core Industrial Services</h2>
        <div className="services-grid">
          {services.map(({ icon: Icon, title, text }) => (
            <article className="service-card" key={title}>
              <Icon className="service-icon" size={34} strokeWidth={1.8} />
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <footer className="site-footer" id="contact">
        <p>&copy; 2026 TechLogic S.p.A. - All rights reserved.</p>
      </footer>

      <ChatWidget />
    </main>
  );
}

export default App;
