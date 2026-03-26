"use client";
import { PlaneTakeoff, Shield, Globe } from "lucide-react";
import { DARK_THEME } from "@/lib/auth-utils";

export default function BrandPanel() {
  return (
    <div
      className="hidden md:flex flex-col justify-between p-12 relative overflow-hidden"
      style={{
        background: `linear-gradient(145deg, ${DARK_THEME.bg} 0%, #0D1F3C 40%, #061730 100%)`,
        flex: "0 0 45%",
      }}
    >
      {/* Decorative Mesh Blobs */}
      <div className="absolute w-[500px] h-[500px] rounded-full top-[-120px] left-[-120px] blur-[100px]" 
           style={{ background: `${DARK_THEME.primary}15` }} />
      
      <div className="relative z-10">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2.5 rounded-xl shadow-lg" style={{ background: `linear-gradient(135deg, ${DARK_THEME.primary}, ${DARK_THEME.secondary})` }}>
            <PlaneTakeoff size={24} color="#0B132B" />
          </div>
          <span className="text-2xl font-bold tracking-tight text-white font-serif">Aura</span>
        </div>
        <p className="text-[11px] font-bold tracking-[0.2em] uppercase opacity-50">AI Travel Intelligence</p>
      </div>

      <div className="relative z-10 space-y-6">
        <h1 className="text-5xl font-bold leading-tight text-white font-serif">
          Travel at the <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">
            speed of thought.
          </span>
        </h1>
        <p className="text-slate-400 max-w-xs leading-relaxed">
          Your AI companion that plans, adapts, and secures your journey in real-time.
        </p>
      </div>

      <div className="relative z-10 flex gap-6 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
        <span className="flex items-center gap-2"><Shield size={14} className="text-cyan-500" /> SOC 2 Secure</span>
        <span className="flex items-center gap-2"><Globe size={14} className="text-cyan-500" /> 190+ Countries</span>
      </div>
    </div>
  );
}