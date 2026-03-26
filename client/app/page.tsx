import Link from "next/link";
import { PlaneTakeoff, Sparkles, ArrowRight, Shield, Globe } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0B132B] text-white font-sans selection:bg-cyan-500/30">
      {/* Navigation */}
      <nav className="flex justify-between items-center px-8 py-6 max-w-7-xl mx-auto">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-cyan-400 to-blue-600 p-2 rounded-xl shadow-lg shadow-cyan-500/20">
            <PlaneTakeoff size={24} className="text-[#0B132B]" />
          </div>
          <span className="text-2xl font-bold font-serif tracking-tight">Aura</span>
        </div>
        <Link href="/auth">
          <button className="text-sm font-bold text-cyan-400 hover:text-white transition-colors">
            Sign In
          </button>
        </Link>
      </nav>

      {/* Hero Section */}
      <main className="flex flex-col items-center justify-center text-center px-6 pt-20 pb-32 relative overflow-hidden">
        {/* Background Glows */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(circle_at_50%_20%,rgba(76,201,240,0.1),transparent_50%)] pointer-events-none" />
        
        <div className="relative z-10 space-y-8 max-w-4xl">
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-1.5 rounded-full text-xs font-bold tracking-wide text-cyan-400 uppercase">
            <Sparkles size={14} /> Agentic AI Travel Engine
          </div>
          
          <h1 className="text-6xl md:text-8xl font-bold font-serif leading-[1.1] tracking-tighter">
            Travel at the <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400">
              speed of thought.
            </span>
          </h1>
          
          <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Stop planning. Start experiencing. AURA is your autonomous travel agent that orchestrates logistics, 
            compliance, and local insights in seconds.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link href="/auth">
              <button className="bg-white text-[#0B132B] px-8 py-4 rounded-2xl font-bold text-lg flex items-center gap-2 hover:bg-cyan-400 transition-all hover:scale-105 active:scale-95 shadow-xl shadow-white/5">
                Launch My Journey <ArrowRight size={20} />
              </button>
            </Link>
          </div>
        </div>
      </main>

      {/* Trust Bar */}
      <div className="border-t border-white/5 bg-white/[0.02] py-8">
        <div className="max-w-7xl mx-auto px-8 flex flex-wrap justify-center gap-8 md:gap-16 opacity-40 grayscale hover:grayscale-0 transition-all duration-700">
          <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-widest"><Shield size={16} /> SOC 2 Secure</div>
          <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-widest"><Globe size={16} /> Global Reach</div>
          <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-widest"><Sparkles size={16} /> LLM Optimized</div>
        </div>
      </div>
    </div>
  );
}