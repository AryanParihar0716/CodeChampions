"use client";
import { useState } from "react";
import { AlertCircle, ArrowRight } from "lucide-react";
import { DARK_THEME } from "@/lib/auth-utils";

export function FloatingInput({ label, type = "text", value, onChange, error, icon: Icon, rightSlot, id }: any) {
  const [focused, setFocused] = useState(false);
  const hasValue = value.length > 0;

  return (
    <div className="relative w-full">
      <div
        style={{
          borderColor: error ? DARK_THEME.error : focused ? DARK_THEME.primary : DARK_THEME.border,
          backgroundColor: "rgba(255,255,255,0.04)",
          boxShadow: focused ? `0 0 0 3px ${DARK_THEME.primary}22` : "none",
          transition: "all 0.2s ease",
        }}
        className="relative flex items-center rounded-2xl border px-4 h-14 gap-2"
      >
        {Icon && <Icon size={17} style={{ color: focused ? DARK_THEME.primary : DARK_THEME.textSecondary }} />}
        <div className="relative flex-1">
          <label
            htmlFor={id}
            style={{
              color: error ? DARK_THEME.error : focused ? DARK_THEME.primary : DARK_THEME.textSecondary,
              fontSize: focused || hasValue ? "10px" : "14px",
              top: focused || hasValue ? "4px" : "50%",
              transform: focused || hasValue ? "none" : "translateY(-50%)",
              transition: "all 0.18s ease",
            }}
            className="absolute left-0 font-medium tracking-wide pointer-events-none"
          >
            {label}
          </label>
          <input
            id={id} type={type} value={value}
            onChange={(e) => onChange(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            style={{ color: DARK_THEME.textPrimary }}
            className="w-full outline-none border-none bg-transparent pt-3.5 text-sm font-medium"
          />
        </div>
        {rightSlot}
      </div>
      {error && (
        <p style={{ color: DARK_THEME.error }} className="mt-1.5 ml-1 text-[11.5px] flex items-center gap-1 font-medium">
          <AlertCircle size={11} /> {error}
        </p>
      )}
    </div>
  );
}

export function PrimaryButton({ children, onClick, loading = false }: any) {
  const [hover, setHover] = useState(false);
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover
          ? `linear-gradient(135deg, ${DARK_THEME.primaryHover}, ${DARK_THEME.secondary})`
          : `linear-gradient(135deg, ${DARK_THEME.primary}, ${DARK_THEME.secondary})`,
        boxShadow: hover ? `0 8px 28px ${DARK_THEME.primary}55` : `0 4px 18px ${DARK_THEME.primary}33`,
        transform: hover ? "translateY(-1px)" : "none",
      }}
      className="w-full h-14 rounded-2xl text-[#0B132B] font-bold text-[15px] tracking-wide flex items-center justify-center gap-2 transition-all duration-200"
    >
      {loading ? (
        <div className="w-5 h-5 border-2 border-[#0B132B] border-t-transparent rounded-full animate-spin" />
      ) : (
        <>{children} <ArrowRight size={16} /></>
      )}
    </button>
  );
}