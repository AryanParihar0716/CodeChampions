/*"use client";

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
      {/* Sidebar }
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
          onClick={() => {
            // Clear authentication token
            document.cookie = "aura_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
            window.location.href = "/auth";
          }}
          className="flex items-center gap-3 p-3 text-rose-500 hover:text-rose-400 transition-all"
        >
          <LogOut size={18} /> Sign Out
        </button>
      </aside>

      {/* Main Chat Area }
      <main className="flex-1 flex flex-col relative">
        <header className="p-6 border-b border-white/5 flex justify-between items-center">
          <h2 className="text-sm font-mono text-cyan-500 tracking-widest uppercase">
            Agentic Console // V2.0
          </h2>
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> Agent Core Online
          </div>
        </header>

        {/* Chat Messages }
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

                {/* ===== AGENT RESPONSE CARDS ===== }

                {/* VISA CARD }
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

                {/* FLIGHT CARDS }
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

                {/* HOTEL CARDS }
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

                {/* WEATHER CARD }
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

        {/* Input Bar }
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
}*/
/*"use client";
import { useState } from "react";
import { Send, Plane, Hotel, ShieldCheck, MapPin } from "lucide-react";

export default function Dashboard() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages(prev => [...prev, { role: "user", text: input }]);
    
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "bot", ...data }]);
    } catch (e) {
      console.error("Agent Offline");
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className="min-h-screen bg-[#0B132B] text-white flex flex-col p-6">
      <div className="flex-1 max-w-5xl mx-auto w-full space-y-8 overflow-y-auto pb-32">
        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
            <div className={`p-4 rounded-2xl max-w-[80%] ${m.role === 'user' ? 'bg-cyan-600' : 'bg-white/5 border border-white/10'}`}>
              {m.text || `Syncing data for ${m.destination}...`}
            </div>

            {/* Flight Cards }
            {m.flight_result?.flights?.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 w-full">
                {m.flight_result.flights.map((f:any, idx:number) => (
                  <div key={idx} className="bg-white/5 p-4 rounded-xl border border-white/10 flex items-center gap-3">
                    <img src={f.logo} className="w-8 h-8 bg-white rounded p-1" />
                    <div>
                      <p className="text-xs font-bold">{f.airline}</p>
                      <p className="text-xs text-cyan-400 font-mono">{f.price}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Hotel Cards }
            {m.hotel_result?.hotels?.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 w-full">
                {m.hotel_result.hotels.map((h:any, idx:number) => (
                  <div key={idx} className="bg-white/5 rounded-xl overflow-hidden border border-white/10">
                    <img src={h.image} className="h-24 w-full object-cover opacity-70" />
                    <div className="p-3">
                      <p className="text-xs font-bold truncate">{h.name}</p>
                      <p className="text-[10px] text-cyan-400">INR {h.price}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="text-cyan-400 animate-pulse text-sm font-mono">ORCHESTRATING AGENTS...</div>}
      </div>

      {/* Fixed Input Area }
      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 w-full max-w-3xl px-6">
        <div className="relative">
          <input 
            value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Ask AURA: 'Find hotels and flights for Dubai'"
            className="w-full bg-white/10 border border-white/10 p-5 rounded-2xl outline-none focus:border-cyan-500 text-white"
          />
          <button onClick={handleSend} className="absolute right-4 top-1/2 -translate-y-1/2 bg-cyan-500 p-2 rounded-xl text-[#0B132B]">
            <Send size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}*/
/*"use client";
import { useState } from "react";
import { Send, Plane, Hotel, ShieldCheck, MapPin, Bot, Sparkles, Clock, Star, CloudSun } from "lucide-react";

export default function Dashboard() {
  const [messages, setMessages] = useState<any[]>([
    { role: "bot", reply: "AURA Online. Where are we heading today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages(prev => [...prev, { role: "user", text: input }]);
    
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "bot", ...data }]);
    } catch (e) {
      console.error("Agent Offline");
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className="min-h-screen bg-[#0B132B] text-white flex flex-col p-6">
      <div className="flex-1 max-w-5xl mx-auto w-full space-y-8 overflow-y-auto pb-32">
        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
            <div className={`p-4 rounded-2xl max-w-[80%] ${m.role === 'user' ? 'bg-cyan-600' : 'bg-white/5 border border-white/10'}`}>
              {m.text || m.reply || `Syncing data for ${m.destination}...`}
            </div>

            {/* Flight Cards }
            {m.flight_result?.flights?.length > 0 && (
              <div className="w-full mt-4 space-y-2">
                <p className="text-[10px] uppercase tracking-widest text-indigo-400 font-bold ml-1">Live Flight Intelligence</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {m.flight_result.flights.map((f:any, idx:number) => (
                    <div key={idx} className="bg-white/5 p-4 rounded-xl border border-white/10 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                         <Plane size={18} className="text-indigo-400" />
                         <div>
                           <p className="text-xs font-bold">{f.airline}</p>
                           <p className="text-[10px] text-slate-500">BOM → {m.destination}</p>
                         </div>
                      </div>
                      <p className="text-sm font-bold text-indigo-400">{f.price}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Hotel Cards }
            {m.hotel_result?.hotels?.length > 0 && (
              <div className="w-full mt-6 space-y-2">
                <p className="text-[10px] uppercase tracking-widest text-amber-400 font-bold ml-1">Verified Accommodations</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {m.hotel_result.hotels.map((h:any, idx:number) => (
                    <div key={idx} className="bg-white/5 rounded-xl overflow-hidden border border-white/10">
                      <img src={h.image} className="h-24 w-full object-cover opacity-60" />
                      <div className="p-3 flex justify-between items-center">
                        <p className="text-xs font-bold truncate max-w-[100px]">{h.name}</p>
                        <p className="text-xs text-amber-400 font-mono">INR {h.price}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
        {loading && <div className="text-cyan-400 animate-pulse text-sm font-mono flex items-center gap-2"><Sparkles size={14}/> ORCHESTRATING AGENTS...</div>}
      </div>

      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 w-full max-w-3xl px-6">
        <div className="relative group">
          <input 
            value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Ask AURA: 'Find hotels and flights for Dubai'"
            className="w-full bg-white/5 border border-white/10 p-5 rounded-2xl outline-none focus:border-cyan-500 text-white transition-all"
          />
          <button onClick={handleSend} className="absolute right-4 top-1/2 -translate-y-1/2 bg-cyan-500 p-2 rounded-xl text-[#0B132B] hover:scale-105 active:scale-95 transition-all">
            <Send size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}*/
/*"use client";
import { useState } from "react";
import { Send, Plane, Hotel, Sparkles } from "lucide-react";

export default function Dashboard() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages(prev => [...prev, { role: "user", text: input }]);
    
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "bot", ...data }]);
    } catch (e) { console.error("Offline"); }
    finally { setLoading(false); setInput(""); }
  };

  return (
    <div className="min-h-screen bg-[#0B132B] text-white flex flex-col p-6">
      <div className="flex-1 max-w-5xl mx-auto w-full space-y-8 overflow-y-auto pb-32">
        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
            <div className={`p-4 rounded-2xl max-w-[80%] ${m.role === 'user' ? 'bg-cyan-600' : 'bg-white/5 border border-white/10'}`}>
              {m.text || m.reply}
            </div>

            {m.flight_result?.flights?.map((f:any, idx:number) => (
              <div key={idx} className="w-full max-w-md mt-2 bg-white/5 p-4 rounded-xl border border-white/10 flex items-center justify-between animate-in slide-in-from-left">
                <div className="flex items-center gap-3">
                  <img src={f.logo} className="w-8 h-8 bg-white p-1 rounded" />
                  <p className="text-sm font-bold">{f.airline}</p>
                </div>
                <p className="text-cyan-400 font-mono">{f.price}</p>
              </div>
            ))}

            <div className="grid grid-cols-2 gap-4 mt-4 w-full">
              {m.hotel_result?.hotels?.map((h:any, idx:number) => (
                <div key={idx} className="bg-white/5 rounded-xl overflow-hidden border border-white/10">
                  <img src={h.image} className="h-24 w-full object-cover" />
                  <div className="p-3 flex justify-between">
                    <p className="text-xs font-bold truncate">{h.name}</p>
                    <p className="text-xs text-amber-400">INR {h.price}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
        {loading && <div className="text-cyan-400 animate-pulse text-sm font-mono flex items-center gap-2"><Sparkles size={14}/> ORCHESTRATING...</div>}
      </div>

      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 w-full max-w-3xl px-6">
        <input 
          value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          placeholder="Try: 'Dubai next week' or 'Tokyo May 10th to 15th'"
          className="w-full bg-white/5 border border-white/10 p-5 rounded-2xl outline-none focus:border-cyan-500 text-white"
        />
      </div>
    </div>
  );
}*/
/*"use client";
import { useState } from "react";
import { 
  Send, Plane, Hotel, ShieldCheck, CloudSun, 
  Sparkles, Bot, Clock, Star, MapPin 
} from "lucide-react";

export default function Dashboard() {
  const [messages, setMessages] = useState<any[]>([
    { role: "bot", reply: "AURA Agents Online. Where are we heading? I'll run live checks for your journey." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const userQuery = input;
    setMessages(prev => [...prev, { role: "user", text: userQuery }]);
    setInput("");

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userQuery }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "bot", ...data }]);
    } catch (e) {
      console.error("Agent Core Offline");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B132B] text-white flex flex-col p-6 font-sans">
      {/* Header }
      <header className="max-w-5xl mx-auto w-full flex justify-between items-center mb-8 border-b border-white/5 pb-4">
        <div className="flex items-center gap-2">
          <Plane className="text-cyan-400 rotate-45" size={24} />
          <h1 className="text-xl font-bold tracking-tighter">AURA <span className="text-cyan-500 text-xs">V3.0</span></h1>
        </div>
        <div className="flex items-center gap-2 text-[10px] text-slate-500 uppercase tracking-widest">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> Agentic Stream Active
        </div>
      </header>

      {/* Chat Space }
      <div className="flex-1 max-w-5xl mx-auto w-full space-y-8 overflow-y-auto pb-40 px-2 custom-scrollbar">
        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'} animate-in fade-in slide-in-from-bottom-2`}>
            {/* Main Text Bubble }
            <div className={`p-4 rounded-2xl max-w-[85%] text-sm ${
              m.role === 'user' ? 'bg-cyan-600 shadow-lg shadow-cyan-500/20' : 'bg-white/5 border border-white/10'
            }`}>
              {m.text || m.reply || `Synthesizing live data for ${m.destination}...`}
            </div>

            {/* --- AGENT CARDS GRID --- }
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 w-full max-w-4xl">
              
              {/* VISA CARD (Dynamic) }
              {m.visa_result && (
                <div className="bg-gradient-to-r from-cyan-500/20 to-transparent border-l-4 border-cyan-400 p-4 rounded-r-xl">
                  <div className="flex items-center gap-2 mb-1">
                    <ShieldCheck size={14} className="text-cyan-400" />
                    <span className="text-[10px] font-bold text-cyan-500 uppercase tracking-wider">{m.visa_result.agent}</span>
                  </div>
                  <p className="text-xs font-bold text-white mb-1">{m.visa_result.status}</p>
                  <p className="text-[11px] text-slate-400 leading-relaxed line-clamp-2">{m.visa_result.detail}</p>
                </div>
              )}

              {/* WEATHER CARD (Dynamic) }
              {m.weather_result && (
                <div className="bg-gradient-to-r from-emerald-500/20 to-transparent border-l-4 border-emerald-400 p-4 rounded-r-xl">
                  <div className="flex items-center gap-2 mb-1">
                    <CloudSun size={14} className="text-emerald-400" />
                    <span className="text-[10px] font-bold text-emerald-500 uppercase tracking-wider">Environment Intelligence</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <p className="text-2xl font-bold">{m.weather_result.temp}</p>
                    <p className="text-[11px] text-slate-300 capitalize">{m.weather_result.condition}</p>
                  </div>
                </div>
              )}
            </div>

            {/* FLIGHTS ROW (Dynamic) }
            {m.flight_result?.flights?.length > 0 && (
              <div className="w-full mt-4 space-y-2">
                <p className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest ml-1">Live Flight Options</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {m.flight_result.flights.map((f:any, idx:number) => (
                    <div key={idx} className="bg-white/5 p-3 rounded-xl border border-white/5 flex items-center justify-between hover:border-indigo-500/50 transition-all">
                      <div className="flex items-center gap-3">
                        <img src={f.logo} className="w-8 h-8 bg-white p-1 rounded" alt="airline" />
                        <div>
                          <p className="text-[11px] font-bold">{f.airline}</p>
                          <p className="text-[9px] text-slate-500">BOM → {m.destination}</p>
                        </div>
                      </div>
                      <p className="text-xs font-bold text-indigo-300">{f.price}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* HOTELS ROW (Dynamic) }
            {m.hotel_result?.hotels?.length > 0 && (
              <div className="w-full mt-6 space-y-2">
                <p className="text-[10px] font-bold text-amber-400 uppercase tracking-widest ml-1">Premium Stays</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {m.hotel_result.hotels.map((h:any, idx:number) => (
                    <div key={idx} className="bg-white/5 rounded-xl overflow-hidden border border-white/5 group hover:border-amber-500/50 transition-all">
                      <div className="h-20 w-full overflow-hidden">
                        <img src={h.image} className="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition-all" alt="hotel" />
                      </div>
                      <div className="p-2 flex justify-between items-center">
    <p className="text-[10px] font-bold truncate max-w-[100px]">{h.name}</p>
    <p className="text-[10px] text-amber-400 font-mono">
      {h.price} {/* ✅ Just h.price! The API will send '$54' or '£165' }
    </p>
  </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 text-cyan-400 animate-pulse text-xs font-mono">
            <Sparkles size={14} className="animate-spin" /> ORCHESTRATING AGENTS...
          </div>
        )}
      </div>

      {/* Input Console }
      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 w-full max-w-3xl px-6">
        <div className="relative group">
          <input 
            value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Try: 'Tokyo next Friday' or 'Hotels in Paris for 5 days'..."
            className="w-full bg-white/5 border border-white/10 p-5 rounded-2xl outline-none focus:border-cyan-500 text-sm transition-all focus:bg-white/[0.07]"
          />
          <button onClick={handleSend} className="absolute right-4 top-1/2 -translate-y-1/2 bg-cyan-500 p-2 rounded-xl text-[#0B132B] hover:scale-105 active:scale-95 transition-all">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}*/
/*"use client";
import { useState } from "react";
import { 
  Send, Plane, Hotel, ShieldCheck, CloudSun, 
  Sparkles, Bot, Clock, Star, MapPin 
} from "lucide-react";

export default function Dashboard() {
  const [messages, setMessages] = useState<any[]>([
    { role: "bot", reply: "AURA Agents Online. Where are we heading? I'll run live checks for your journey." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const userQuery = input;
    setMessages(prev => [...prev, { role: "user", text: userQuery }]);
    setInput("");

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userQuery }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "bot", ...data }]);
    } catch (e) {
      console.error("Agent Core Offline");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B132B] text-white flex flex-col p-6 font-sans overflow-x-hidden">
      {/* Header }
      <header className="max-w-5xl mx-auto w-full flex justify-between items-center mb-8 border-b border-white/5 pb-4">
        <div className="flex items-center gap-2">
          <Plane className="text-cyan-400 rotate-45" size={24} />
          <h1 className="text-xl font-bold tracking-tighter italic">AURA <span className="text-cyan-500 text-xs not-italic">V3.0</span></h1>
        </div>
        <div className="flex items-center gap-2 text-[10px] text-slate-500 uppercase tracking-widest">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> Agentic Stream Active
        </div>
      </header>

      {/* Chat Space }
      <div className="flex-1 max-w-5xl mx-auto w-full space-y-8 overflow-y-auto pb-40 px-2">
        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'} animate-in fade-in slide-in-from-bottom-2`}>
            {/* Main Text Bubble }
            <div className={`p-4 rounded-2xl max-w-[85%] text-sm ${
              m.role === 'user' ? 'bg-cyan-600 shadow-lg shadow-cyan-500/20' : 'bg-white/5 border border-white/10 text-slate-200'
            }`}>
              {m.text || m.reply || `Synthesizing live data for ${m.destination}...`}
            </div>

            {/* --- AGENT CARDS GRID --- }
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 w-full max-w-4xl">
              
              {/* VISA CARD }
              {m.visa_result && (
                <div className="bg-gradient-to-r from-cyan-500/20 to-transparent border-l-4 border-cyan-400 p-4 rounded-r-xl">
                  <div className="flex items-center gap-2 mb-1">
                    <ShieldCheck size={14} className="text-cyan-400" />
                    <span className="text-[10px] font-bold text-cyan-500 uppercase tracking-wider">Visa Intelligence</span>
                  </div>
                  <p className="text-xs font-bold text-white mb-1">{m.visa_result.status}</p>
                  <p className="text-[11px] text-slate-400 leading-relaxed line-clamp-2">{m.visa_result.detail}</p>
                </div>
              )}

              {/* WEATHER CARD }
              {m.weather_result && (
                <div className="bg-gradient-to-r from-emerald-500/20 to-transparent border-l-4 border-emerald-400 p-4 rounded-r-xl">
                  <div className="flex items-center gap-2 mb-1">
                    <CloudSun size={14} className="text-emerald-400" />
                    <span className="text-[10px] font-bold text-emerald-500 uppercase tracking-wider">Atmospheric Data</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <p className="text-2xl font-bold">{m.weather_result.temp}</p>
                    <p className="text-[11px] text-slate-300 capitalize">{m.weather_result.condition}</p>
                  </div>
                </div>
              )}
            </div>

            {/* FLIGHTS ROW }
            {m.flight_result?.flights?.length > 0 && (
              <div className="w-full mt-4 space-y-2">
                <p className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest ml-1">Live Flight Options</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {m.flight_result.flights.map((f:any, idx:number) => (
                    <div key={idx} className="bg-white/5 p-3 rounded-xl border border-white/5 flex items-center justify-between hover:border-indigo-500/50 transition-all">
                      <div className="flex items-center gap-3">
                        {f.logo ? <img src={f.logo} className="w-8 h-8 bg-white p-1 rounded" alt="" /> : <Plane size={16}/>}
                        <div>
                          <p className="text-[11px] font-bold">{f.airline}</p>
                          <p className="text-[9px] text-slate-500">BOM → {m.destination}</p>
                        </div>
                      </div>
                      <p className="text-xs font-bold text-indigo-300">{f.price}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* HOTELS ROW }
            {m.hotel_result?.hotels?.length > 0 && (
              <div className="w-full mt-6 space-y-2 pb-4">
                <p className="text-[10px] font-bold text-amber-400 uppercase tracking-widest ml-1">Curated Accommodations</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {m.hotel_result.hotels.map((h:any, idx:number) => (
                    <div key={idx} className="bg-white/5 rounded-xl overflow-hidden border border-white/5 group hover:border-amber-500/50 transition-all">
                      <div className="h-24 w-full overflow-hidden">
                        <img src={h.image || "https://images.unsplash.com/photo-1566073771259-6a8506099945"} className="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition-all" alt="" />
                      </div>
                      <div className="p-3 flex justify-between items-center">
                        <p className="text-[11px] font-bold truncate max-w-[120px]">{h.name}</p>
                        <p className="text-[11px] text-amber-400 font-mono">
                          {/* 🚀 DYNAMIC CURRENCY: No hardcoded '₹' here }
                          {h.price}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 text-cyan-400 animate-pulse text-xs font-mono">
            <Sparkles size={14} className="animate-spin" /> SYNTHESIZING JOURNEY NODES...
          </div>
        )}
      </div>

      {/* Input Console }
      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 w-full max-w-3xl px-6">
        <div className="relative group shadow-2xl">
          <input 
            value={input} onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Search: 'Paris next month' or 'Dubai in May'..."
            className="w-full bg-white/5 border border-white/10 p-5 rounded-2xl outline-none focus:border-cyan-500 text-sm transition-all focus:bg-white/[0.08] backdrop-blur-md"
          />
          <button onClick={handleSend} className="absolute right-4 top-1/2 -translate-y-1/2 bg-cyan-500 p-2 rounded-xl text-[#0B132B] hover:scale-105 active:scale-95 transition-all">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}*/
/*"use client";
import { useState, useEffect } from "react";
import { 
  Send, Plane, Hotel, ShieldCheck, CloudSun, 
  Sparkles, Moon, Sun, MapPin, Compass, Briefcase
} from "lucide-react";

export default function Dashboard() {
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [messages, setMessages] = useState<any[]>([
    { role: "bot", reply: "Systems Primed. AURA Intelligence is online. Where shall we explore?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Smooth theme transition effect
  const toggleTheme = () => setTheme(prev => prev === "dark" ? "light" : "dark");

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    const userQuery = input;
    setMessages(prev => [...prev, { role: "user", text: userQuery }]);
    setInput("");

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userQuery }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "bot", ...data }]);
    } catch (e) { console.error("Agent Core Offline"); } 
    finally { setLoading(false); }
  };

  return (
    <div className={`min-h-screen transition-colors duration-500 font-sans ${
      theme === "dark" ? "bg-[#0B132B] text-white" : "bg-slate-50 text-slate-900"
    }`}>
      
      {/* --- PREMIUM HEADER --- }
      <header className={`sticky top-0 z-50 backdrop-blur-md border-b transition-colors ${
        theme === "dark" ? "bg-[#0B132B]/80 border-white/5" : "bg-white/80 border-slate-200"
      }`}>
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2 group cursor-pointer">
            <div className="p-2 bg-cyan-500 rounded-lg group-hover:rotate-12 transition-transform">
              <Plane className="text-white" size={20} />
            </div>
            <h1 className="text-xl font-black tracking-tighter">AURA <span className="text-cyan-500">3.0</span></h1>
          </div>
          
          <div className="flex items-center gap-6">
            <nav className="hidden md:flex gap-4 text-xs font-bold uppercase tracking-widest opacity-60">
              <span className="hover:text-cyan-500 cursor-pointer">Explore</span>
              <span className="hover:text-cyan-500 cursor-pointer">History</span>
            </nav>
            <button 
              onClick={toggleTheme}
              className={`p-2 rounded-full transition-all ${
                theme === "dark" ? "bg-white/5 hover:bg-white/10" : "bg-slate-200 hover:bg-slate-300"
              }`}
            >
              {theme === "dark" ? <Sun size={18} className="text-amber-400" /> : <Moon size={18} className="text-indigo-600" />}
            </button>
          </div>
        </div>
      </header>

      {/* --- CHAT CANVAS --- }
      <div className="max-w-4xl mx-auto w-full px-6 pt-10 pb-40 space-y-10">
        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'} animate-in fade-in slide-in-from-bottom-4 duration-500`}>
            
            {/* Message Bubble }
            <div className={`px-5 py-4 rounded-2xl shadow-sm text-sm leading-relaxed max-w-[85%] ${
              m.role === 'user' 
                ? 'bg-gradient-to-br from-cyan-500 to-blue-600 text-white shadow-cyan-500/20' 
                : theme === "dark" ? 'bg-white/5 border border-white/10' : 'bg-white border border-slate-200 shadow-xl shadow-slate-200/50'
            }`}>
              {m.text || m.reply || `Analyzing travel vectors for ${m.destination}...`}
            </div>

            {/* --- AGENT OUTPUTS --- }
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 w-full">
              
              {/* VISA CARD }
              {m.visa_result && (
                <div className={`p-5 rounded-2xl border-l-4 transition-all hover:scale-[1.02] ${
                  theme === "dark" ? "bg-white/5 border-cyan-500" : "bg-white border-slate-200 border-l-cyan-500 shadow-md"
                }`}>
                  <div className="flex items-center gap-2 mb-3">
                    <ShieldCheck size={16} className="text-cyan-500" />
                    <span className="text-[10px] font-black uppercase tracking-widest opacity-60">Visa Compliance</span>
                  </div>
                  <h4 className="font-bold text-sm mb-1">{m.visa_result.status}</h4>
                  <p className="text-[11px] opacity-70 leading-relaxed">{m.visa_result.detail}</p>
                </div>
              )}

              {/* WEATHER CARD }
              {m.weather_result && (
                <div className={`p-5 rounded-2xl border-l-4 transition-all hover:scale-[1.02] ${
                  theme === "dark" ? "bg-white/5 border-emerald-500" : "bg-white border-slate-200 border-l-emerald-500 shadow-md"
                }`}>
                  <div className="flex items-center gap-2 mb-3">
                    <CloudSun size={16} className="text-emerald-500" />
                    <span className="text-[10px] font-black uppercase tracking-widest opacity-60">Atmosphere</span>
                  </div>
                  <div className="flex items-baseline gap-2">
                    <span className="text-3xl font-black">{m.weather_result.temp}</span>
                    <span className="text-xs opacity-60 capitalize">{m.weather_result.condition}</span>
                  </div>
                </div>
              )}
            </div>

            {/* FLIGHT LIST }
            {m.flight_result?.flights?.length > 0 && (
              <div className="w-full mt-6 space-y-3">
                <div className="flex items-center gap-2 opacity-40 px-1">
                  <Briefcase size={12}/> <span className="text-[10px] font-black uppercase tracking-[0.2em]">Verified Air Routes</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {m.flight_result.flights.map((f:any, idx:number) => (
                    <div key={idx} className={`p-4 rounded-2xl flex flex-col gap-3 transition-all hover:shadow-lg ${
                      theme === "dark" ? "bg-white/5 border border-white/5" : "bg-white border border-slate-100 shadow-sm"
                    }`}>
                      <div className="flex justify-between items-center">
                        <img src={f.logo} className="h-6 w-auto grayscale contrast-125 opacity-80" alt="" />
                        <span className="text-xs font-mono font-bold text-cyan-500">{f.price}</span>
                      </div>
                      <p className="text-[11px] font-bold opacity-80">{f.airline}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* HOTEL GALLERY }
            {m.hotel_result?.hotels?.length > 0 && (
              <div className="w-full mt-8 space-y-3">
                <div className="flex items-center gap-2 opacity-40 px-1">
                  <Compass size={12}/> <span className="text-[10px] font-black uppercase tracking-[0.2em]">Luxe Accommodations</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {m.hotel_result.hotels.map((h:any, idx:number) => (
                    <div key={idx} className={`rounded-3xl overflow-hidden transition-all hover:-translate-y-1 ${
                      theme === "dark" ? "bg-white/5" : "bg-white shadow-xl shadow-slate-200/50"
                    }`}>
                      <div className="h-28 w-full relative">
                        <img src={h.image} className="w-full h-full object-cover" alt="" />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                        <span className="absolute bottom-2 right-3 text-[10px] font-mono text-white bg-black/40 px-2 py-1 rounded-full backdrop-blur-sm">
                          {h.price}
                        </span>
                      </div>
                      <div className="p-3">
                        <p className="text-[11px] font-bold truncate">{h.name}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-3 text-cyan-500 animate-pulse text-xs font-black tracking-widest uppercase">
            <Sparkles size={14} className="animate-spin" /> Orchestrating Intelligence...
          </div>
        )}
      </div>

      {/* --- FLOATING COMMAND CONSOLE --- }
      <div className={`fixed bottom-0 left-0 right-0 p-8 flex justify-center backdrop-blur-sm transition-colors ${
        theme === "dark" ? "bg-gradient-to-t from-[#0B132B] to-transparent" : "bg-gradient-to-t from-white to-transparent"
      }`}>
        <div className={`relative w-full max-w-3xl flex items-center transition-all group ${
          theme === "dark" ? "focus-within:scale-[1.01]" : "focus-within:scale-[1.01]"
        }`}>
          <input 
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Ask AURA: 'Next month in Tokyo' or 'Hotels for London'..."
            className={`w-full py-5 pl-8 pr-20 rounded-3xl outline-none text-sm transition-all border shadow-2xl ${
              theme === "dark" 
                ? "bg-white/10 border-white/10 text-white placeholder:text-slate-600 focus:border-cyan-500 focus:bg-white/15" 
                : "bg-white border-slate-200 text-slate-900 placeholder:text-slate-400 focus:border-cyan-500 shadow-slate-300/50"
            }`}
          />
          <button 
            onClick={handleSend}
            className="absolute right-3 p-3 bg-cyan-500 rounded-2xl text-white hover:bg-cyan-400 hover:rotate-12 transition-all shadow-lg shadow-cyan-500/40"
          >
            <Send size={20} />
          </button>
        </div>
      </div>

      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0, 186, 255, 0.2); border-radius: 10px; }
      `}</style>
    </div>
  );
}*/
"use client";
import { useState, useEffect } from "react";
import { Send, Plane, Hotel, ShieldCheck, CloudSun, Sparkles, Moon, Sun, Briefcase, Compass, Clock } from "lucide-react";

export default function Dashboard() {
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [mounted, setMounted] = useState(false);
  const [messages, setMessages] = useState<any[]>([{ role: "bot", reply: "AURA Online. Where shall we explore?" }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => { setMounted(true); }, []);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages(prev => [...prev, { role: "user", text: input }]);
    const query = input; setInput("");
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: "bot", ...data }]);
    } catch (e) { console.error("Offline"); } finally { setLoading(false); }
  };

  if (!mounted) return <div className="min-h-screen bg-[#0B132B]" />;

  return (
    <div className={`min-h-screen transition-all duration-500 ${theme === "dark" ? "bg-[#0B132B] text-white" : "bg-slate-50 text-slate-900"}`}>
      <header className={`sticky top-0 z-50 backdrop-blur-md border-b p-4 ${theme === "dark" ? "bg-[#0B132B]/80 border-white/5" : "bg-white/80 border-slate-200"}`}>
        <div className="max-w-5xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2"><Plane className="text-cyan-500 rotate-45"/><h1 className="font-black italic">AURA 3.0</h1></div>
          <button onClick={() => setTheme(t => t === 'dark' ? 'light' : 'dark')} className="p-2 rounded-full bg-white/5">{theme === 'dark' ? <Sun size={18}/> : <Moon size={18}/>}</button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto p-6 pb-40 space-y-8">
        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'} animate-in slide-in-from-bottom-2`}>
            <div className={`p-4 rounded-2xl text-sm ${m.role === 'user' ? 'bg-cyan-600' : 'bg-white/5 border border-white/10'}`}>{m.text || m.reply}</div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 w-full">
              {m.visa_result && <AgentCard icon={<ShieldCheck/>} title="Visa" status={m.visa_result.status} detail={m.visa_result.detail} theme={theme} />}
              {m.weather_result && <AgentCard icon={<CloudSun/>} title="Weather" status={m.weather_result.temp} detail={m.weather_result.condition} theme={theme} />}
            </div>

            {m.flight_result?.flights?.length > 0 && (
              <div className="w-full mt-6 grid grid-cols-1 md:grid-cols-3 gap-3">
                {m.flight_result.flights.map((f:any, idx:number) => (
                  <div key={idx} className="p-4 rounded-2xl bg-white/5 border border-white/5 flex justify-between items-center hover:border-cyan-500/50 transition-all">
                    <div className="flex items-center gap-2">{f.logo ? <img src={f.logo} className="w-6 h-6 grayscale"/> : <Plane size={14}/>}<p className="text-[10px] font-bold">{f.airline}</p></div>
                    <p className="text-xs font-mono text-cyan-400">{f.price}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </main>

      <div className="fixed bottom-8 left-0 right-0 p-6 flex justify-center">
        <div className="relative w-full max-w-2xl">
          <input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleSend()} placeholder="Ask AURA..." className="w-full p-5 rounded-3xl bg-white/10 border border-white/10 backdrop-blur-xl outline-none focus:border-cyan-500 transition-all" />
          <button onClick={handleSend} className="absolute right-3 top-1/2 -translate-y-1/2 p-3 bg-cyan-500 rounded-2xl text-white"><Send size={18}/></button>
        </div>
      </div>
    </div>
  );
}

function AgentCard({ icon, title, status, detail, theme }: any) {
  return (
    <div className={`p-4 rounded-2xl border-l-4 transition-all hover:scale-[1.01] ${theme === 'dark' ? 'bg-white/5 border-cyan-500' : 'bg-white border-slate-200 border-l-cyan-500 shadow-md'}`}>
      <div className="flex items-center gap-2 mb-2 opacity-60 text-[10px] uppercase font-bold">{icon} {title}</div>
      <p className="text-sm font-bold">{status}</p>
      <p className="text-[11px] opacity-70 mt-1 line-clamp-2">{detail}</p>
    </div>
  );
}