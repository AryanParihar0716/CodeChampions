"use client";

import { useState } from "react";
import {
  PlaneTakeoff, Send, Bot, ShieldCheck, Sparkles, LogOut,
  History, Plane, Hotel, CloudSun, Star, Clock, ArrowRight,
} from "lucide-react";

// --- Type Definitions ---
interface FlightData {
  airline: string;
  price: string;
  duration: string;
  departure: string;
  stops: string;
}

interface HotelData {
  name: string;
  stars: number;
  price_per_night: string;
  amenities: string[];
  rating: number;
}

interface AgentResult {
  agent: string;
  destination: string;
  [key: string]: unknown;
}

interface Message {
  role: "user" | "bot";
  text: string;
  visa?: AgentResult;
  flights?: AgentResult & { flights: FlightData[] };
  hotels?: AgentResult & { hotels: HotelData[] };
  weather?: AgentResult & { temp: string; condition: string; best_season: string; tip: string };
  intent?: string;
}

export default function Dashboard() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "bot",
      text: "AURA Agents active. Where are we heading? I'll run visa, flight, hotel & weather checks instantly.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input;

    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ message: userMsg }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.reply,
          visa: data.visa,
          flights: data.flights,
          hotels: data.hotels,
          weather: data.weather,
          intent: data.intent,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Connection to Agent Core lost. Is the server running?" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#0B132B] text-white font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/5 bg-white/[0.02] flex flex-col p-6 hidden md:flex">
        <div className="flex items-center gap-3 mb-12">
          <PlaneTakeoff className="text-cyan-400" size={28} />
          <span className="text-2xl font-bold font-serif">Aura</span>
        </div>
        <nav className="flex-1 space-y-2">
          <button className="flex items-center gap-3 w-full p-3 rounded-xl bg-cyan-500/10 text-cyan-400 font-bold">
            <Sparkles size={18} /> New Journey
          </button>
          <button className="flex items-center gap-3 w-full p-3 rounded-xl text-slate-500 hover:text-white transition-all">
            <History size={18} /> Past Travels
          </button>
        </nav>
        <button
          onClick={() => (window.location.href = "/auth")}
          className="flex items-center gap-3 p-3 text-rose-500 hover:text-rose-400 transition-all"
        >
          <LogOut size={18} /> Sign Out
        </button>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative">
        <header className="p-6 border-b border-white/5 flex justify-between items-center">
          <h2 className="text-sm font-mono text-cyan-500 tracking-widest uppercase">
            Agentic Console // V2.0
          </h2>
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> Agent Core Online
          </div>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${
                  msg.role === "bot" ? "bg-cyan-500/20 text-cyan-400" : "bg-white/10"
                }`}
              >
                {msg.role === "bot" ? <Bot size={20} /> : <div className="font-bold text-xs">YOU</div>}
              </div>
              <div className="space-y-3 max-w-[85%]">
                <div
                  className={`p-4 rounded-2xl ${
                    msg.role === "user"
                      ? "bg-cyan-600 text-white"
                      : "bg-white/5 border border-white/10 text-slate-200"
                  }`}
                >
                  {msg.text}
                </div>

                {/* ===== AGENT RESPONSE CARDS ===== */}

                {/* VISA CARD */}
                {msg.visa && (
                  <div className="bg-gradient-to-r from-cyan-500/20 to-transparent border-l-4 border-cyan-400 p-4 rounded-r-xl">
                    <div className="flex items-center gap-2 mb-2">
                      <ShieldCheck size={16} className="text-cyan-400" />
                      <span className="text-[10px] uppercase font-bold tracking-widest text-cyan-500">
                        {msg.visa.agent}
                      </span>
                    </div>
                    <p className="text-sm font-semibold text-white">{String(msg.visa.status)}</p>
                    <p className="text-xs text-slate-400 mt-1">{String(msg.visa.detail)}</p>
                  </div>
                )}

                {/* FLIGHT CARDS */}
                {msg.flights && (
                  <div className="bg-gradient-to-r from-indigo-500/20 to-transparent border-l-4 border-indigo-400 p-4 rounded-r-xl space-y-3">
                    <div className="flex items-center gap-2 mb-1">
                      <Plane size={16} className="text-indigo-400" />
                      <span className="text-[10px] uppercase font-bold tracking-widest text-indigo-400">
                        {msg.flights.agent}
                      </span>
                    </div>
                    {msg.flights.flights.map((f: FlightData, idx: number) => (
                      <div
                        key={idx}
                        className="flex items-center justify-between bg-white/5 rounded-xl p-3 border border-white/5 hover:border-indigo-400/30 transition-all"
                      >
                        <div>
                          <p className="text-sm font-bold text-white">{f.airline}</p>
                          <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
                            <span className="flex items-center gap-1">
                              <Clock size={12} /> {f.departure}
                            </span>
                            <span>{f.duration}</span>
                            <span>{f.stops}</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-lg font-bold text-indigo-300">{f.price}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* HOTEL CARDS */}
                {msg.hotels && (
                  <div className="bg-gradient-to-r from-amber-500/20 to-transparent border-l-4 border-amber-400 p-4 rounded-r-xl space-y-3">
                    <div className="flex items-center gap-2 mb-1">
                      <Hotel size={16} className="text-amber-400" />
                      <span className="text-[10px] uppercase font-bold tracking-widest text-amber-400">
                        {msg.hotels.agent}
                      </span>
                    </div>
                    {msg.hotels.hotels.map((h: HotelData, idx: number) => (
                      <div
                        key={idx}
                        className="bg-white/5 rounded-xl p-3 border border-white/5 hover:border-amber-400/30 transition-all"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div>
                            <p className="text-sm font-bold text-white">{h.name}</p>
                            <div className="flex items-center gap-1 mt-1">
                              {Array.from({ length: h.stars }).map((_, s) => (
                                <Star key={s} size={12} className="text-amber-400 fill-amber-400" />
                              ))}
                              <span className="text-xs text-slate-400 ml-2">{h.rating}/5</span>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-lg font-bold text-amber-300">{h.price_per_night}</p>
                            <p className="text-[10px] text-slate-500">/night</p>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-1 mt-2">
                          {h.amenities.map((a: string, ai: number) => (
                            <span
                              key={ai}
                              className="text-[10px] bg-white/5 px-2 py-0.5 rounded-full text-slate-400"
                            >
                              {a}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* WEATHER CARD */}
                {msg.weather && (
                  <div className="bg-gradient-to-r from-emerald-500/20 to-transparent border-l-4 border-emerald-400 p-4 rounded-r-xl">
                    <div className="flex items-center gap-2 mb-2">
                      <CloudSun size={16} className="text-emerald-400" />
                      <span className="text-[10px] uppercase font-bold tracking-widest text-emerald-400">
                        {msg.weather.agent}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 mb-2">
                      <span className="text-3xl font-bold text-white">{msg.weather.temp}</span>
                      <span className="text-sm text-slate-300">{msg.weather.condition}</span>
                    </div>
                    <div className="space-y-1 text-xs text-slate-400">
                      <p>
                        <span className="text-emerald-400 font-bold">Best Season:</span>{" "}
                        {msg.weather.best_season}
                      </p>
                      <p>
                        <span className="text-emerald-400 font-bold">Pro Tip:</span> {msg.weather.tip}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex items-center gap-3 text-cyan-500 text-xs italic">
              <div className="flex gap-1">
                <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: "0ms" }} />
                <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: "150ms" }} />
                <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
              AURA is orchestrating agents...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-6">
          <div className="max-w-4xl mx-auto relative">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder='Try: "Japan", "flights to Thailand", "hotels in Maldives"...'
              className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 pl-6 pr-14 focus:outline-none focus:border-cyan-400/50 text-white placeholder:text-slate-600"
            />
            <button
              onClick={handleSend}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-cyan-500 rounded-xl text-[#0B132B] hover:bg-cyan-400 transition-all"
            >
              <Send size={20} />
            </button>
          </div>
          <div className="max-w-4xl mx-auto flex items-center justify-center gap-4 mt-3">
            {["visa", "flight", "hotel", "weather"].map((intent) => (
              <span
                key={intent}
                className="text-[10px] uppercase tracking-widest text-slate-600 flex items-center gap-1"
              >
                {intent === "visa" && <ShieldCheck size={10} />}
                {intent === "flight" && <Plane size={10} />}
                {intent === "hotel" && <Hotel size={10} />}
                {intent === "weather" && <CloudSun size={10} />}
                {intent}
              </span>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}