/*"use client";
import { useState } from "react";
import { Bot, Send, PlaneTakeoff } from "lucide-react";

export default function Dashboard() {
  const [chat, setChat] = useState([{ role: "bot", text: "AURA Online. Where are we flying today?" }]);
  const [input, setInput] = useState("");

  const askAgent = async () => {
    const res = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });
    const data = await res.json();
    setChat([...chat, { role: "user", text: input }, { role: "bot", text: `${data.reply} Status: ${data.visa}` }]);
    setInput("");
  };

  return (
    <div className="min-h-screen bg-[#0B132B] text-white p-8">
        <header className="flex justify-between items-center mb-12">
            <div className="flex items-center gap-3">
                <PlaneTakeoff className="text-cyan-400" />
                <h1 className="text-2xl font-serif font-bold">AURA Dashboard</h1>
            </div>
            <div className="bg-white/5 px-4 py-2 rounded-full text-xs font-mono text-cyan-500 border border-cyan-500/20">
                AGENT_STATUS: ACTIVE
            </div>
        </header>

        <div className="max-w-3xl mx-auto space-y-4 h-[60vh] overflow-y-auto mb-6">
            {chat.map((m, i) => (
                <div key={i} className={`p-4 rounded-2xl max-w-[80%] ${m.role === 'bot' ? 'bg-white/5' : 'bg-cyan-600 ml-auto'}`}>
                    {m.text}
                </div>
            ))}
        </div>

        <div className="max-w-3xl mx-auto flex gap-4">
            <input 
                value={input} onChange={e => setInput(e.target.value)}
                className="flex-1 bg-white/5 border border-white/10 rounded-xl p-4 outline-none focus:border-cyan-500"
                placeholder="Enter destination..."
            />
            <button onClick={askAgent} className="bg-cyan-500 p-4 rounded-xl text-[#0B132B]"><Send /></button>
        </div>
    </div>
  );
}*/
/*"use client";
import { PlaneTakeoff, ShieldCheck, Send } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#0B132B] text-white p-10 flex flex-col items-center">
      <header className="w-full max-w-5xl flex justify-between items-center mb-20">
        <div className="flex items-center gap-3">
          <PlaneTakeoff size={32} className="text-cyan-400" />
          <h1 className="text-3xl font-serif font-bold">AURA Command</h1>
        </div>
        <div className="bg-cyan-500/10 border border-cyan-500/20 px-4 py-2 rounded-full flex items-center gap-2">
            <ShieldCheck size={16} className="text-cyan-400" />
            <span className="text-xs font-bold text-cyan-400 uppercase tracking-widest">Authenticated Session</span>
        </div>
      </header>

      <main className="text-center space-y-6 animate-in fade-in zoom-in duration-700">
        <h2 className="text-5xl font-bold">Welcome Home, Traveler.</h2>
        <p className="text-slate-400 text-lg max-w-md mx-auto">
          Your personal AI agent is now standing by to plan your next global experience.
        </p>
        
        {/* Placeholder for the Chat UI we built earlier }
        <div className="mt-12 w-full max-w-2xl bg-white/5 border border-white/10 p-12 rounded-3xl border-dashed">
            <p className="text-slate-600 font-medium italic">Agentic Chat Interface Initializing...</p>
        </div>
      </main>
    </div>
  );
}*/
/*"use client";
import { PlaneTakeoff, Sparkles } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-[#0B132B] flex flex-col items-center justify-center text-white p-6">
      <div className="p-4 bg-cyan-500/10 rounded-full mb-8 animate-pulse">
        <PlaneTakeoff size={48} className="text-cyan-400" />
      </div>
      <h1 className="text-5xl font-serif font-bold tracking-tight mb-4">AURA Online</h1>
      <p className="text-slate-400 text-xl max-w-lg text-center leading-relaxed">
        Your authentication is complete. The agents are currently mapping your global travel footprint.
      </p>
      
      <div className="mt-12 flex items-center gap-2 text-cyan-400 font-mono text-sm tracking-widest uppercase bg-white/5 px-6 py-2 rounded-full border border-cyan-400/20">
        <Sparkles size={14} /> Agentic Sync: 100%
      </div>
    </div>
  );
}*/
/*"use client";

import { useState } from "react";
import { PlaneTakeoff, Send, Bot, ShieldCheck, Sparkles, LogOut, History } from "lucide-react";
import { DARK_THEME } from "@/lib/auth-utils";

export default function Dashboard() {
  const [messages, setMessages] = useState([
    { role: "bot", text: "AURA Agents active. Where are we heading? I'll run the compliance checks for your Indian passport immediately." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setMessages(prev => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg }),
      });
      const data = await res.json();
      
      setMessages(prev => [...prev, { 
        role: "bot", 
        text: data.reply, 
        visa: data.visa // This matches your Python logic
      }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: "bot", text: "Connection to Agent Core lost. Is the server running?" }]);
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
        <button onClick={() => window.location.href = "/auth"} className="flex items-center gap-3 p-3 text-rose-500 hover:text-rose-400 transition-all">
          <LogOut size={18} /> Sign Out
        </button>
      </aside>

      {/* Main Chat Area }
      <main className="flex-1 flex flex-col relative">
        <header className="p-6 border-b border-white/5 flex justify-between items-center">
            <h2 className="text-sm font-mono text-cyan-500 tracking-widest uppercase">Agentic Console // V1.0</h2>
            <div className="flex items-center gap-2 text-xs text-slate-500">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> Agent Core Online
            </div>
        </header>

        {/* Chat Messages }
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${msg.role === "bot" ? "bg-cyan-500/20 text-cyan-400" : "bg-white/10"}`}>
                {msg.role === "bot" ? <Bot size={20} /> : <div className="font-bold text-xs">YOU</div>}
              </div>
              <div className="space-y-3 max-w-[80%]">
                <div className={`p-4 rounded-2xl ${msg.role === "user" ? "bg-cyan-600" : "bg-white/5 border border-white/10"}`}>
                  {msg.text}
                </div>
                {/* AGENTIC VISA CARD }
                {msg.visa && (
                  <div className="bg-gradient-to-r from-cyan-500/20 to-transparent border-l-4 border-cyan-400 p-4 rounded-r-xl animate-in slide-in-from-left-4 duration-500">
                    <div className="flex items-center gap-2 mb-1">
                        <ShieldCheck size={16} className="text-cyan-400" />
                        <span className="text-[10px] uppercase font-bold tracking-widest text-cyan-500">Compliance Agent</span>
                    </div>
                    <p className="text-sm font-semibold">{msg.visa}</p>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && <div className="text-cyan-500 animate-pulse text-xs italic">AURA is orchestrating agents...</div>}
        </div>

        {/* Input Bar }
        <div className="p-6">
          <div className="max-w-4xl mx-auto relative">
            <input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Enter destination (e.g. Thailand, Japan, France...)"
              className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 pl-6 pr-14 focus:outline-none focus:border-cyan-400/50 transition-all"
            />
            <button 
              onClick={handleSend}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-cyan-500 rounded-xl text-[#0B132B] hover:bg-cyan-400 transition-all"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}*/
"use client";

import { useState } from "react";
import { PlaneTakeoff, Send, Bot, ShieldCheck, Sparkles, LogOut, History } from "lucide-react";

// 1. THE FIX: Define the structure of a message
interface Message {
  role: "user" | "bot";
  text: string;
  visa?: string; // The "?" means this is optional
}

export default function Dashboard() {
  // 2. THE FIX: Explicitly tell the state to use the Message type
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: "bot", 
      text: "AURA Agents active. Where are we heading? I'll run the compliance checks for your Indian passport immediately." 
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    
    // Add User Message
    setMessages(prev => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg }),
      });
      
      const data = await res.json();
      
      // 3. THE FIX: This now works because TypeScript knows 'visa' is allowed
      setMessages(prev => [...prev, { 
        role: "bot", 
        text: data.reply, 
        visa: data.visa 
      }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: "bot", text: "Connection to Agent Core lost. Is the server running?" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#0B132B] text-white font-sans overflow-hidden">
      {/* Sidebar - Same as before */}
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
        <button onClick={() => window.location.href = "/auth"} className="flex items-center gap-3 p-3 text-rose-500 hover:text-rose-400 transition-all">
          <LogOut size={18} /> Sign Out
        </button>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative">
        <header className="p-6 border-b border-white/5 flex justify-between items-center">
            <h2 className="text-sm font-mono text-cyan-500 tracking-widest uppercase">Agentic Console // V1.0</h2>
            <div className="flex items-center gap-2 text-xs text-slate-500">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> Agent Core Online
            </div>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${msg.role === "bot" ? "bg-cyan-500/20 text-cyan-400" : "bg-white/10"}`}>
                {msg.role === "bot" ? <Bot size={20} /> : <div className="font-bold text-xs">YOU</div>}
              </div>
              <div className="space-y-3 max-w-[80%]">
                <div className={`p-4 rounded-2xl ${msg.role === "user" ? "bg-cyan-600 text-white" : "bg-white/5 border border-white/10 text-slate-200"}`}>
                  {msg.text}
                </div>
                
                {/* AGENTIC VISA CARD */}
                {msg.visa && (
                  <div className="bg-gradient-to-r from-cyan-500/20 to-transparent border-l-4 border-cyan-400 p-4 rounded-r-xl animate-in slide-in-from-left-4 duration-500">
                    <div className="flex items-center gap-2 mb-1">
                        <ShieldCheck size={16} className="text-cyan-400" />
                        <span className="text-[10px] uppercase font-bold tracking-widest text-cyan-500">Compliance Agent</span>
                    </div>
                    <p className="text-sm font-semibold text-white">{msg.visa}</p>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && <div className="text-cyan-500 animate-pulse text-xs italic">AURA is orchestrating agents...</div>}
        </div>

        {/* Input Bar */}
        <div className="p-6">
          <div className="max-w-4xl mx-auto relative">
            <input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Enter destination (e.g. Thailand, Japan, France...)"
              className="w-full bg-white/5 border border-white/10 rounded-2xl p-4 pl-6 pr-14 focus:outline-none focus:border-cyan-400/50 text-white"
            />
            <button 
              onClick={handleSend}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-cyan-500 rounded-xl text-[#0B132B] hover:bg-cyan-400 transition-all"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}