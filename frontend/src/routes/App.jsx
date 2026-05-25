import {
  BotMessageSquare,
  CircleGauge,
  Microscope,
  Send,
  Truck,
  X,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";

const BACKEND_URL =
  import.meta.env.VITE_BACKEND_URL ?? "http://localhost:9998/agent";

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

const heroBackground = {
  backgroundImage:
    "linear-gradient(rgb(0 0 0 / 0.7), rgb(0 0 0 / 0.7)), url('https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=1600')",
};

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
      throw new Error(
        `Server returned unexpected error state: ${response.status}`,
      );
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
    <div className={`mb-4 flex items-start ${isUser ? "justify-end" : ""}`}>
      <div
        className={`max-w-[80%] whitespace-pre-line rounded-2xl p-3 text-sm leading-[1.45] shadow-sm ${
          isUser
            ? "rounded-tr-none bg-blue-600 text-white"
            : "rounded-tl-none border border-gray-200 bg-white text-gray-700"
        }`}
      >
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
      <button
        className="group fixed right-4 bottom-4 z-60 flex h-14 min-w-14 cursor-pointer items-center justify-center gap-0 overflow-hidden rounded-full border-0 bg-blue-600 p-4 text-white shadow-[0_20px_35px_rgb(15_23_42/0.28)] transition-[background,gap] duration-200 hover:gap-2 hover:bg-blue-700 md:right-6 md:bottom-6"
        type="button"
        onClick={() => setIsOpen((current) => !current)}
      >
        <BotMessageSquare size={24} />
        <span className="max-w-0 overflow-hidden font-semibold whitespace-nowrap transition-[max-width] duration-300 group-hover:max-w-36">
          Chat Support
        </span>
      </button>

      {isOpen && (
        <aside
          className="fixed right-4 bottom-22 z-60 flex h-[min(500px,calc(100vh-132px))] w-[min(384px,calc(100vw-32px))] flex-col overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-[0_25px_50px_rgb(15_23_42/0.25)] md:right-6 md:bottom-24"
          aria-label="TechLogic AI chat"
        >
          <div className="flex items-center justify-between gap-4 bg-blue-600 p-4 text-white">
            <div className="flex items-center gap-3">
              <div className="grid h-8 min-w-8 place-items-center rounded-lg bg-white text-xs font-extrabold text-blue-600 shadow-inner">
                TL
              </div>
              <div>
                <h3 className="m-0 text-sm tracking-normal">
                  AI Assistant | TechLogic
                </h3>
                <div className="flex items-center gap-1.5 text-xs text-blue-100">
                  <span className="h-2 w-2 animate-pulse rounded-full bg-green-400" />
                  Online & Connected
                </div>
              </div>
            </div>
            <button
              className="grid h-8 w-8 cursor-pointer place-items-center rounded-lg border-0 bg-transparent text-blue-100 hover:bg-blue-500 hover:text-white"
              type="button"
              aria-label="Close chat"
              onClick={() => setIsOpen(false)}
            >
              <X size={20} />
            </button>
          </div>

          <div
            className="flex-1 overflow-y-auto bg-slate-50 p-4 [scrollbar-color:#cbd5e1_transparent] scrollbar-thin [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-thumb]:rounded-sm [&::-webkit-scrollbar-thumb]:bg-slate-300 [&::-webkit-scrollbar-track]:bg-transparent"
            ref={messagesRef}
          >
            {messages.map((message) => (
              <ChatBubble
                key={message.id}
                text={message.text}
                isUser={message.isUser}
              />
            ))}
          </div>

          {isLoading && (
            <div className="flex items-center gap-2 border-t border-gray-100 bg-slate-50 px-4 py-2 text-xs text-gray-400 italic">
              <span className="h-4 w-4 animate-spin rounded-full border-3 border-blue-200 border-t-blue-600" />
              <span>[Retrieval & Agent Inference in progress]...</span>
            </div>
          )}

          <form
            className="flex items-center gap-2 border-t border-gray-100 bg-white p-3"
            onSubmit={handleSubmit}
          >
            <input
              className="min-w-0 flex-1 rounded-xl border border-gray-200 bg-gray-50 px-4 py-2.5 text-sm outline-0 transition-[border,background] focus:border-blue-500 focus:bg-white"
              ref={inputRef}
              type="text"
              placeholder="Type your question here..."
              autoComplete="off"
              value={inputValue}
              onChange={(event) => setInputValue(event.target.value)}
            />
            <button
              className="grid size-10.5 cursor-pointer place-items-center rounded-xl border-0 bg-blue-600 text-white shadow-[0_8px_14px_rgb(37_99_235/0.25)] transition-colors hover:not-disabled:bg-blue-700 disabled:cursor-wait disabled:opacity-70"
              type="submit"
              aria-label="Send message"
              disabled={isLoading}
            >
              <Send className="rotate-45" size={20} />
            </button>
          </form>
        </aside>
      )}
    </>
  );
}

function App() {
  return (
    <main className="min-h-screen bg-gray-50 text-gray-800">
      <nav className="sticky top-0 z-50 flex items-start justify-between gap-6 bg-white px-4 py-3.5 shadow-md md:items-center md:px-6 md:py-4">
        <div className="text-2xl leading-none font-extrabold text-blue-600">
          TECH<span className="text-blue-700">LOGIC</span>
        </div>
        <div className="hidden gap-6 font-medium text-gray-700 md:flex">
          <a className="hover:text-blue-600" href="#services">
            Products
          </a>
          <a className="hover:text-blue-600" href="#services">
            Quality Control
          </a>
          <a className="hover:text-blue-600" href="#company">
            Company
          </a>
          <a className="hover:text-blue-600" href="#contact">
            Contact Us
          </a>
        </div>
        <a
          className="inline-flex min-h-10.5 cursor-pointer items-center justify-center rounded-lg bg-blue-600 px-3.5 py-2.5 text-white transition-colors hover:bg-blue-700 md:px-5"
          href="#contact"
        >
          Get a Quote
        </a>
      </nav>

      <header
        className="flex min-h-115 items-center justify-center bg-cover bg-center px-6 py-16 text-center text-white md:min-h-125"
        style={heroBackground}
      >
        <div className="max-w-205">
          <h1 className="m-0 mb-4 text-[clamp(2.5rem,6vw,3.75rem)] leading-[1.05] font-bold">
            Precision in Every Detail
          </h1>
          <p className="mx-auto mb-8 max-w-175 text-base leading-relaxed text-gray-200 md:text-[1.2rem]">
            High-quality mechanical components for modern industry. 24/7
            technical support powered by our virtual AI assistant.
          </p>
          <a
            href="#services"
            className="inline-flex min-h-12 cursor-pointer items-center justify-center rounded-full bg-white px-8 py-3 font-extrabold text-blue-900 transition hover:-translate-y-px hover:bg-gray-100"
          >
            Explore Products
          </a>
        </div>
      </header>

      <section id="services" className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="m-0 mb-12 text-center text-3xl font-bold text-gray-900">
          Our Core Industrial Services
        </h2>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {services.map(({ icon: Icon, title, text }) => (
            <article
              className="min-h-57.5 rounded-lg border border-gray-100 bg-white p-8 shadow-sm transition hover:-translate-y-0.5 hover:shadow-xl"
              key={title}
            >
              <Icon
                className="mb-4 text-blue-500"
                size={34}
                strokeWidth={1.8}
              />
              <h3 className="m-0 mb-2 text-xl font-bold text-gray-900">
                {title}
              </h3>
              <p className="m-0 leading-relaxed text-gray-600">{text}</p>
            </article>
          ))}
        </div>
      </section>

      <footer
        className="bg-gray-900 px-6 py-10 text-center text-white"
        id="contact"
      >
        <p className="m-0">
          &copy; 2026 TechLogic S.p.A. - All rights reserved.
        </p>
      </footer>

      <ChatWidget />
    </main>
  );
}

export default App;
