import {
  ArrowRight,
  BotMessageSquare,
  CircleGauge,
  Clock,
  Cog,
  Mail,
  MapPin,
  Microscope,
  Phone,
  ScanSearch,
  Ruler,
  Send,
  ShieldCheck,
  ClipboardCheck,
  Timer,
  Truck,
  X,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link, Outlet } from "react-router-dom";

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

const products = [
  {
    name: "Micro Turned Fasteners",
    category: "Precision hardware",
    description:
      "Miniature screws, bushings, pins, and threaded inserts for compact industrial assemblies.",
    specs: [
      "0.8-12 mm diameter",
      "Steel, brass, aluminum",
      "Batch traceability",
    ],
    icon: Cog,
  },
  {
    name: "Telemetry Sensor Bodies",
    category: "Inspection systems",
    description:
      "Machined housings and calibration-ready mounts for laser-vision quality control lines.",
    specs: [
      "CNC finished",
      "Low-vibration geometry",
      "Optical alignment support",
    ],
    icon: Ruler,
  },
  {
    name: "Zero-Defect Stock Lines",
    category: "Ready-to-ship components",
    description:
      "Validated stock components with documented dimensional checks for urgent production needs.",
    specs: [
      "24/48h EU delivery",
      "Inspection certificates",
      "Recurring supply plans",
    ],
    icon: ShieldCheck,
  },
];

const heroBackground = {
  backgroundImage:
    "linear-gradient(rgb(0 0 0 / 0.7), rgb(0 0 0 / 0.7)), url('https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=1600')",
};

const companyHeroImage =
  "https://images.unsplash.com/photo-1565043666747-69f6646db940?auto=format&fit=crop&q=80&w=1600";

const companyPhotos = [
  {
    src: "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&q=80&w=900",
    alt: "Precision machining floor with industrial equipment",
  },
  {
    src: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=900",
    alt: "Engineer reviewing industrial production data",
  },
  {
    src: "https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?auto=format&fit=crop&q=80&w=900",
    alt: "Technician inspecting components in a manufacturing lab",
  },
];

const homePhotos = [
  {
    src: "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&q=80&w=1200",
    alt: "Industrial production floor with precision machinery",
  },
  {
    src: "https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&q=80&w=900",
    alt: "Technician inspecting a machined component",
  },
];

const qualityHeroImage =
  "https://images.unsplash.com/photo-1581092334651-ddf26d9a09d0?auto=format&fit=crop&q=80&w=1600";

const qualitySteps = [
  {
    title: "Incoming Material Checks",
    text: "Material lots are reviewed before machining so every batch starts with verified traceability.",
    icon: ClipboardCheck,
  },
  {
    title: "In-Process Measurement",
    text: "Critical dimensions are monitored during production to catch drift before it reaches final inspection.",
    icon: Ruler,
  },
  {
    title: "Final Vision Review",
    text: "Laser and camera-assisted checks validate surface, geometry, and batch consistency before release.",
    icon: ScanSearch,
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

export function HomePage() {
  return (
    <>
      <header
        className="flex min-h-125 items-center bg-cover bg-center px-6 py-16 text-white md:min-h-150"
        style={heroBackground}
      >
        <div className="mx-auto grid max-w-6xl grid-cols-1 gap-10 md:grid-cols-[1fr_0.8fr] md:items-end">
          <div>
            <p className="mb-4 inline-flex rounded-full border border-white/25 bg-white/10 px-4 py-2 text-sm font-semibold text-blue-100 backdrop-blur">
              Industrial components with AI-assisted support
            </p>
            <h1 className="m-0 max-w-3xl text-[clamp(2.75rem,7vw,4.75rem)] leading-[0.98] font-bold">
              Precision in every detail
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-relaxed text-gray-100 md:text-xl">
              High-quality mechanical components for modern industry, backed by
              documented inspection, express logistics, and a 24/7 virtual
              technical assistant.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link
                to="/products"
                className="inline-flex min-h-12 items-center justify-center gap-2 rounded-lg bg-white px-6 py-3 font-extrabold text-blue-900 transition hover:-translate-y-px hover:bg-gray-100"
              >
                Explore Products
                <ArrowRight size={18} />
              </Link>
              <Link
                to="/quality-control"
                className="inline-flex min-h-12 items-center justify-center rounded-lg border border-white/40 px-6 py-3 font-bold text-white transition hover:bg-white/10"
              >
                View Quality Process
              </Link>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3 rounded-lg border border-white/20 bg-white/10 p-4 backdrop-blur">
            <div>
              <p className="m-0 text-3xl font-bold">24/48h</p>
              <p className="mt-1 text-sm text-blue-100">EU logistics</p>
            </div>
            <div>
              <p className="m-0 text-3xl font-bold">3</p>
              <p className="mt-1 text-sm text-blue-100">Control stages</p>
            </div>
            <div>
              <p className="m-0 text-3xl font-bold">AI</p>
              <p className="mt-1 text-sm text-blue-100">Support desk</p>
            </div>
          </div>
        </div>
      </header>

      <section className="mx-auto grid max-w-6xl grid-cols-1 gap-10 px-6 py-16 md:grid-cols-[0.95fr_1.05fr] md:items-center md:py-20">
        <div className="grid gap-4">
          <img
            className="h-80 w-full rounded-lg object-cover shadow-lg"
            src={homePhotos[0].src}
            alt={homePhotos[0].alt}
          />
          <div className="grid grid-cols-[0.8fr_1fr] gap-4">
            <img
              className="h-44 w-full rounded-lg object-cover shadow-sm"
              src={homePhotos[1].src}
              alt={homePhotos[1].alt}
            />
            <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
              <p className="m-0 text-sm font-bold tracking-wide text-blue-600 uppercase">
                Built for repeatability
              </p>
              <p className="mt-3 text-2xl font-bold text-gray-950">
                From micro-parts to inspected stock lines.
              </p>
            </div>
          </div>
        </div>

        <div>
          <p className="mb-3 text-sm font-bold tracking-wide text-blue-600 uppercase">
            How TechLogic Works
          </p>
          <h2 className="m-0 text-3xl leading-tight font-bold text-gray-950 md:text-5xl">
            Production support that stays close to the details
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-gray-600">
            We help engineering and procurement teams source precision
            components with fewer delays. Drawings, tolerances, batch history,
            inspection notes, and delivery expectations are handled as one
            connected workflow.
          </p>
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2">
            {[
              "Drawing and feasibility review",
              "CNC production planning",
              "Dimensional inspection",
              "Fast quotation support",
            ].map((item) => (
              <div
                className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white p-4 shadow-sm"
                key={item}
              >
                <ShieldCheck className="shrink-0 text-blue-600" size={20} />
                <span className="font-semibold text-gray-800">{item}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="services" className="bg-white px-6 py-16 md:py-20">
        <div className="mx-auto max-w-6xl">
          <div className="mb-10 flex flex-col justify-between gap-5 md:flex-row md:items-end">
            <div>
              <p className="mb-3 text-sm font-bold tracking-wide text-blue-600 uppercase">
                Core Services
              </p>
              <h2 className="m-0 max-w-2xl text-3xl font-bold text-gray-950 md:text-4xl">
                The essential capabilities behind every order
              </h2>
            </div>
            <Link
              className="inline-flex items-center gap-2 font-bold text-blue-700 hover:text-blue-900"
              to="/company"
            >
              Learn about the company
              <ArrowRight size={18} />
            </Link>
          </div>

          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            {services.map(({ icon: Icon, title, text }) => (
              <article
                className="min-h-57.5 rounded-lg border border-gray-200 bg-gray-50 p-8 shadow-sm transition hover:-translate-y-0.5 hover:bg-white hover:shadow-xl"
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
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-16 md:py-20">
        <div className="rounded-lg bg-gray-950 p-8 text-white md:p-10">
          <div className="grid grid-cols-1 gap-8 md:grid-cols-[1fr_0.8fr] md:items-center">
            <div>
              <p className="mb-3 text-sm font-bold tracking-wide text-blue-300 uppercase">
                Always available
              </p>
              <h2 className="m-0 text-3xl font-bold md:text-4xl">
                Ask product and process questions from anywhere on the site
              </h2>
              <p className="mt-4 leading-relaxed text-gray-300">
                The chat assistant connects to the backend agent endpoint and
                helps users explore products, documentation, process details,
                and support requests without leaving the page.
              </p>
            </div>
            <div className="rounded-lg border border-white/10 bg-white/5 p-6">
              <p className="m-0 text-sm font-semibold text-blue-200">
                Try asking:
              </p>
              <ul className="mt-4 space-y-3 p-0 text-gray-200">
                <li>"Which product line supports urgent orders?"</li>
                <li>"How does your inspection workflow work?"</li>
                <li>"Can I request a recurring batch quote?"</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export function ProductsPage() {
  return (
    <section className="bg-gray-50">
      <div className="mx-auto max-w-6xl px-6 py-14 md:py-20">
        <div className="max-w-3xl">
          <p className="mb-3 text-sm font-bold tracking-wide text-blue-600 uppercase">
            Product Lines
          </p>
          <h1 className="m-0 text-4xl leading-tight font-bold text-gray-950 md:text-5xl">
            Precision components for demanding production environments
          </h1>
          <p className="mt-5 text-lg leading-relaxed text-gray-600">
            Explore TechLogic products built around tight tolerances, repeatable
            inspection, and reliable supply for modern industrial teams.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-6 md:grid-cols-3">
          {products.map(
            ({ name, category, description, specs, icon: Icon }) => (
              <article
                className="flex min-h-96 flex-col rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-xl"
                key={name}
              >
                <div className="mb-5 grid size-12 place-items-center rounded-lg bg-blue-50 text-blue-600">
                  <Icon size={26} strokeWidth={1.8} />
                </div>
                <p className="mb-2 text-sm font-semibold text-blue-600">
                  {category}
                </p>
                <h2 className="m-0 text-2xl font-bold text-gray-950">{name}</h2>
                <p className="mt-4 leading-relaxed text-gray-600">
                  {description}
                </p>
                <div className="mt-auto pt-6">
                  <h3 className="mb-3 text-sm font-bold text-gray-900">
                    Key specs
                  </h3>
                  <ul className="m-0 space-y-2 p-0 text-sm text-gray-600">
                    {specs.map((spec) => (
                      <li className="flex items-center gap-2" key={spec}>
                        <span className="size-1.5 rounded-full bg-blue-500" />
                        {spec}
                      </li>
                    ))}
                  </ul>
                </div>
              </article>
            ),
          )}
        </div>

        <div className="mt-10 flex flex-col items-start justify-between gap-5 rounded-lg border border-gray-200 bg-white p-6 md:flex-row md:items-center">
          <div>
            <h2 className="m-0 text-2xl font-bold text-gray-950">
              Need a custom drawing or recurring batch?
            </h2>
            <p className="mt-2 text-gray-600">
              Send a request through the assistant or contact the team for a
              quotation.
            </p>
          </div>
          <a
            className="inline-flex min-h-11 items-center gap-2 rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
            href="#contact"
          >
            <Timer size={18} />
            Request a Quote
          </a>
        </div>
      </div>
    </section>
  );
}

export function CompanyPage() {
  return (
    <section className="bg-gray-50">
      <div className="relative min-h-96 overflow-hidden bg-gray-900 px-6 py-20 text-white">
        <img
          className="absolute inset-0 h-full w-full object-cover opacity-45"
          src={companyHeroImage}
          alt="Modern industrial production facility"
        />
        <div className="relative mx-auto max-w-6xl">
          <p className="mb-3 text-sm font-bold tracking-wide text-blue-200 uppercase">
            Company
          </p>
          <h1 className="m-0 max-w-3xl text-4xl leading-tight font-bold md:text-6xl">
            Built for manufacturers who cannot afford uncertainty
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-gray-100">
            TechLogic combines precision machining, documented quality control,
            and responsive technical support to help industrial teams keep
            production moving.
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-6 py-16 md:py-20">
        <div className="grid grid-cols-1 gap-10 md:grid-cols-[1.1fr_0.9fr] md:items-center">
          <div>
            <p className="mb-3 text-sm font-bold tracking-wide text-blue-600 uppercase">
              What We Do
            </p>
            <h2 className="m-0 text-3xl leading-tight font-bold text-gray-950 md:text-4xl">
              From drawing review to repeatable delivery
            </h2>
            <p className="mt-5 text-lg leading-relaxed text-gray-600">
              We support customers through the full component lifecycle:
              feasibility checks, material selection, CNC production,
              dimensional inspection, documentation, and logistics planning.
              Every workflow is designed to reduce ambiguity before parts reach
              the line.
            </p>
            <p className="mt-4 text-lg leading-relaxed text-gray-600">
              Our team works with procurement, engineering, and quality managers
              who need small parts delivered with clear tolerances, fast
              answers, and reliable batch history.
            </p>
          </div>

          <div className="grid gap-4">
            <img
              className="h-64 w-full rounded-lg object-cover shadow-lg"
              src={companyPhotos[0].src}
              alt={companyPhotos[0].alt}
            />
            <div className="grid grid-cols-2 gap-4">
              {companyPhotos.slice(1).map((photo) => (
                <img
                  className="h-40 w-full rounded-lg object-cover shadow-sm"
                  src={photo.src}
                  alt={photo.alt}
                  key={photo.src}
                />
              ))}
            </div>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-6 md:grid-cols-3">
          <article className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <h3 className="m-0 text-2xl font-bold text-gray-950">Precision</h3>
            <p className="mt-3 leading-relaxed text-gray-600">
              Tight tolerances, stable processes, and inspection-first
              production for critical mechanical components.
            </p>
          </article>
          <article className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <h3 className="m-0 text-2xl font-bold text-gray-950">
              Traceability
            </h3>
            <p className="mt-3 leading-relaxed text-gray-600">
              Batch records, certificates, and clear quality documentation help
              teams move faster during audits and line checks.
            </p>
          </article>
          <article className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <h3 className="m-0 text-2xl font-bold text-gray-950">Support</h3>
            <p className="mt-3 leading-relaxed text-gray-600">
              Technical support and AI-assisted guidance keep product questions,
              drawing requests, and urgent orders moving.
            </p>
          </article>
        </div>
      </div>
    </section>
  );
}

export function QualityControlPage() {
  return (
    <section className="bg-gray-50">
      <div className="relative overflow-hidden bg-gray-950 px-6 py-20 text-white">
        <img
          className="absolute inset-0 h-full w-full object-cover opacity-40"
          src={qualityHeroImage}
          alt="Quality control engineer inspecting industrial components"
        />
        <div className="relative mx-auto grid max-w-6xl grid-cols-1 gap-10 md:grid-cols-[1fr_0.75fr] md:items-end">
          <div>
            <p className="mb-3 text-sm font-bold tracking-wide text-blue-200 uppercase">
              Quality Control
            </p>
            <h1 className="m-0 text-4xl leading-tight font-bold md:text-6xl">
              Inspection designed around zero-defect production
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-relaxed text-gray-100">
              Our quality workflow combines process monitoring, optical
              inspection, and documented batch evidence so teams can approve
              components with confidence.
            </p>
          </div>

          <div className="grid grid-cols-3 gap-3 rounded-lg border border-white/20 bg-white/10 p-4 backdrop-blur">
            <div>
              <p className="m-0 text-3xl font-bold">100%</p>
              <p className="mt-1 text-sm text-blue-100">Traceable batches</p>
            </div>
            <div>
              <p className="m-0 text-3xl font-bold">&micro;m</p>
              <p className="mt-1 text-sm text-blue-100">Tolerance focus</p>
            </div>
            <div>
              <p className="m-0 text-3xl font-bold">24h</p>
              <p className="mt-1 text-sm text-blue-100">Report response</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-6 py-16 md:py-20">
        <div className="max-w-3xl">
          <p className="mb-3 text-sm font-bold tracking-wide text-blue-600 uppercase">
            Inspection Workflow
          </p>
          <h2 className="m-0 text-3xl leading-tight font-bold text-gray-950 md:text-4xl">
            Quality is checked before, during, and after production
          </h2>
        </div>

        <div className="mt-10 grid grid-cols-1 gap-6 md:grid-cols-3">
          {qualitySteps.map(({ title, text, icon: Icon }) => (
            <article
              className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm"
              key={title}
            >
              <div className="mb-5 grid size-12 place-items-center rounded-lg bg-blue-50 text-blue-600">
                <Icon size={26} strokeWidth={1.8} />
              </div>
              <h3 className="m-0 text-2xl font-bold text-gray-950">{title}</h3>
              <p className="mt-4 leading-relaxed text-gray-600">{text}</p>
            </article>
          ))}
        </div>

        <div className="mt-14 grid grid-cols-1 gap-8 rounded-lg border border-gray-200 bg-white p-6 shadow-sm md:grid-cols-[0.9fr_1.1fr] md:p-8">
          <img
            className="h-full min-h-80 w-full rounded-lg object-cover"
            src="https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&q=80&w=1000"
            alt="Technician working with calibrated inspection equipment"
          />
          <div>
            <p className="mb-3 text-sm font-bold tracking-wide text-blue-600 uppercase">
              Documentation
            </p>
            <h2 className="m-0 text-3xl leading-tight font-bold text-gray-950">
              Evidence your quality team can use immediately
            </h2>
            <p className="mt-5 leading-relaxed text-gray-600">
              Every quality package can include dimensional reports, material
              references, batch identifiers, inspection notes, and delivery
              documents. The goal is simple: reduce follow-up loops and keep
              release decisions moving.
            </p>
            <ul className="mt-6 grid grid-cols-1 gap-3 p-0 text-gray-700 sm:grid-cols-2">
              {[
                "Dimensional control reports",
                "Batch and lot traceability",
                "Certificate management",
                "Non-conformity feedback loops",
              ].map((item) => (
                <li className="flex items-center gap-2" key={item}>
                  <ShieldCheck className="text-blue-600" size={18} />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

function App() {
  return (
    <main className="min-h-screen bg-gray-50 text-gray-800">
      <nav className="sticky top-0 z-50 flex items-start justify-between gap-6 bg-white px-4 py-3.5 shadow-md md:items-center md:px-6 md:py-4">
        <Link
          className="text-2xl leading-none font-extrabold text-blue-600"
          to="/"
        >
          TECH<span className="text-blue-700">LOGIC</span>
        </Link>
        <div className="hidden gap-6 font-medium text-gray-700 md:flex">
          <Link className="hover:text-blue-600" to="/products">
            Products
          </Link>
          <Link className="hover:text-blue-600" to="/quality-control">
            Quality Control
          </Link>
          <Link className="hover:text-blue-600" to="/company">
            Company
          </Link>
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

      <Outlet />

      <footer className="bg-gray-900 px-6 py-12 text-white" id="contact">
        <div className="mx-auto grid max-w-6xl grid-cols-1 gap-8 md:grid-cols-[1.2fr_1fr_1fr]">
          <div>
            <h2 className="m-0 text-2xl font-extrabold text-white">
              TECH<span className="text-blue-400">LOGIC</span>
            </h2>
            <p className="mt-4 max-w-md leading-relaxed text-gray-300">
              Precision mechanical components, inspection support, and fast
              technical answers for industrial teams across Europe.
            </p>
          </div>

          <div>
            <h3 className="m-0 mb-4 text-sm font-bold tracking-wide text-blue-300 uppercase">
              Contact Us
            </h3>
            <div className="space-y-3 text-gray-300">
              <a
                className="flex items-center gap-3 transition hover:text-white"
                href="mailto:sales@techlogic.example"
              >
                <Mail size={18} />
                sales@techlogic.example
              </a>
              <a
                className="flex items-center gap-3 transition hover:text-white"
                href="tel:+390212345678"
              >
                <Phone size={18} />
                +39 02 1234 5678
              </a>
              <div className="flex items-start gap-3">
                <MapPin className="mt-0.5 shrink-0" size={18} />
                <span>Via Industria 24, 20100 Milano, Italy</span>
              </div>
            </div>
          </div>

          <div>
            <h3 className="m-0 mb-4 text-sm font-bold tracking-wide text-blue-300 uppercase">
              Support
            </h3>
            <div className="space-y-3 text-gray-300">
              <div className="flex items-center gap-3">
                <Clock size={18} />
                Mon-Fri, 08:30-18:00 CET
              </div>
              <p className="m-0 leading-relaxed">
                For urgent product questions, use the AI assistant in the
                bottom-right corner.
              </p>
            </div>
          </div>
        </div>
        <div className="mx-auto mt-10 max-w-6xl border-t border-white/10 pt-6 text-sm text-gray-400">
          <p className="m-0">
            &copy; 2026 TechLogic S.p.A. - All rights reserved.
          </p>
        </div>
      </footer>

      <ChatWidget />
    </main>
  );
}

export default App;
