import { useState, useRef, useEffect } from "react";
import {
  PlaneTakeoff, Eye, EyeOff, Mail, Phone, Lock, User,
  ArrowRight, RotateCcw, Sparkles, Globe, Apple, ChevronRight,
  Shield, CheckCircle2, AlertCircle, X
} from "lucide-react";

/* ─────────────────────────────────────────────
   DESIGN TOKENS
───────────────────────────────────────────── */
const LIGHT = {
  primary: "#0096C7", primaryHover: "#0077B6", secondary: "#48CAE4",
  bg: "#F7FBFF", surface: "#FFFFFF", border: "#E3F2FD",
  textPrimary: "#1B263B", textSecondary: "#5C677D", error: "#E63946",
};
const DARK = {
  primary: "#4CC9F0", primaryHover: "#3AAED8", secondary: "#4895EF",
  bg: "#0B132B", surface: "#1C2541", border: "#2A3A5E",
  textPrimary: "#E0FBFC", textSecondary: "#A8DADC", error: "#FF4D6D",
};

/* ─────────────────────────────────────────────
   HELPERS
───────────────────────────────────────────── */
const validate = {
  required: (v) => v.trim().length > 0,
  email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
  phone: (v) => /^\+?[\d\s\-()]{7,}$/.test(v),
  password: (v) => v.length >= 6,
  emailOrPhone: (v) => validate.email(v) || validate.phone(v),
};

/* ─────────────────────────────────────────────
   SUB-COMPONENTS
───────────────────────────────────────────── */
function FloatingInput({ label, type = "text", value, onChange, error, icon: Icon, rightSlot, id }) {
  const [focused, setFocused] = useState(false);
  const hasValue = value.length > 0;

  return (
    <div className="relative">
      <div
        style={{
          borderColor: error ? DARK.error : focused ? DARK.primary : DARK.border,
          backgroundColor: "rgba(255,255,255,0.04)",
          boxShadow: focused ? `0 0 0 3px ${DARK.primary}22` : "none",
          transition: "all 0.2s ease",
        }}
        className="relative flex items-center rounded-2xl border px-4 py-0 h-14 gap-2"
      >
        {Icon && (
          <Icon
            size={17}
            style={{ color: focused ? DARK.primary : DARK.textSecondary, flexShrink: 0, transition: "color 0.2s" }}
          />
        )}
        <div className="relative flex-1">
          <label
            htmlFor={id}
            style={{
              color: error ? DARK.error : focused ? DARK.primary : DARK.textSecondary,
              fontSize: focused || hasValue ? "10px" : "14px",
              top: focused || hasValue ? "4px" : "50%",
              transform: focused || hasValue ? "none" : "translateY(-50%)",
              transition: "all 0.18s ease",
              pointerEvents: "none",
            }}
            className="absolute left-0 font-medium tracking-wide"
          >
            {label}
          </label>
          <input
            id={id}
            type={type}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            style={{
              color: DARK.textPrimary,
              background: "transparent",
              paddingTop: "14px",
              fontSize: "14px",
              fontFamily: "inherit",
            }}
            className="w-full outline-none border-none pb-1 font-medium"
          />
        </div>
        {rightSlot}
      </div>
      {error && (
        <p
          style={{ color: DARK.error, fontSize: "11.5px" }}
          className="mt-1.5 ml-1 flex items-center gap-1 font-medium"
        >
          <AlertCircle size={11} />
          {error}
        </p>
      )}
    </div>
  );
}

function PrimaryButton({ children, onClick, loading = false }) {
  const [hover, setHover] = useState(false);
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover
          ? `linear-gradient(135deg, ${DARK.primaryHover}, ${DARK.secondary})`
          : `linear-gradient(135deg, ${DARK.primary}, ${DARK.secondary})`,
        boxShadow: hover ? `0 8px 28px ${DARK.primary}55` : `0 4px 18px ${DARK.primary}33`,
        transform: hover ? "translateY(-1px)" : "none",
        transition: "all 0.22s ease",
      }}
      className="w-full h-14 rounded-2xl text-[#0B132B] font-bold text-[15px] tracking-wide flex items-center justify-center gap-2"
    >
      {loading ? (
        <div className="w-5 h-5 border-2 border-[#0B132B] border-t-transparent rounded-full animate-spin" />
      ) : (
        <>
          {children}
          <ArrowRight size={16} />
        </>
      )}
    </button>
  );
}

function OutlineButton({ children, onClick, icon: Icon }) {
  const [hover, setHover] = useState(false);
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        borderColor: hover ? DARK.primary : DARK.border,
        backgroundColor: hover ? `${DARK.primary}12` : "transparent",
        color: DARK.textPrimary,
        transition: "all 0.2s ease",
      }}
      className="flex-1 h-12 rounded-2xl border flex items-center justify-center gap-2.5 text-[13px] font-semibold"
    >
      {Icon && <Icon size={16} />}
      {children}
    </button>
  );
}

function Divider() {
  return (
    <div className="flex items-center gap-3 my-1">
      <div style={{ flex: 1, height: 1, background: `${DARK.border}` }} />
      <span style={{ color: DARK.textSecondary, fontSize: "12px", fontWeight: 600, letterSpacing: "0.05em" }}>
        OR CONTINUE WITH
      </span>
      <div style={{ flex: 1, height: 1, background: `${DARK.border}` }} />
    </div>
  );
}

/* ─────────────────────────────────────────────
   OTP VIEW
───────────────────────────────────────────── */
function OTPView({ onBack, destination }) {
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [errors, setErrors] = useState({});
  const [resent, setResent] = useState(false);
  const [verified, setVerified] = useState(false);
  const refs = useRef([]);

  const handleChange = (index, val) => {
    if (!/^\d?$/.test(val)) return;
    const next = [...otp];
    next[index] = val;
    setOtp(next);
    if (val && index < 5) refs.current[index + 1]?.focus();
  };

  const handleKeyDown = (index, e) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      refs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e) => {
    const paste = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);
    if (paste.length) {
      const next = [...otp];
      paste.split("").forEach((d, i) => { next[i] = d; });
      setOtp(next);
      refs.current[Math.min(paste.length, 5)]?.focus();
    }
  };

  const handleVerify = () => {
    if (otp.join("").length < 6) {
      setErrors({ otp: "Please enter all 6 digits." });
      return;
    }
    setErrors({});
    setVerified(true);
  };

  const handleResend = () => {
    setOtp(["", "", "", "", "", ""]);
    setResent(true);
    setTimeout(() => setResent(false), 3000);
    refs.current[0]?.focus();
  };

  return (
    <div className="w-full space-y-7">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-1">
          <div
            style={{ background: `${DARK.primary}22`, borderRadius: "12px", padding: "8px" }}
          >
            <Shield size={20} style={{ color: DARK.primary }} />
          </div>
          <h2 style={{ color: DARK.textPrimary, fontFamily: "'Playfair Display', serif", fontSize: "26px", fontWeight: 700 }}>
            Verify your device
          </h2>
        </div>
        <p style={{ color: DARK.textSecondary, fontSize: "14px", lineHeight: 1.6, marginTop: "8px" }}>
          We've sent a 6-digit code to{" "}
          <span style={{ color: DARK.primary, fontWeight: 600 }}>{destination || "your email/phone"}</span>.
          <br />Enter it below to continue.
        </p>
      </div>

      {verified ? (
        <div className="flex flex-col items-center gap-4 py-8">
          <div style={{ background: `${DARK.primary}22`, borderRadius: "50%", padding: "20px" }}>
            <CheckCircle2 size={40} style={{ color: DARK.primary }} />
          </div>
          <p style={{ color: DARK.textPrimary, fontWeight: 700, fontSize: "18px" }}>Verification successful!</p>
          <p style={{ color: DARK.textSecondary, fontSize: "13px" }}>Welcome to Aura. Your journey begins now.</p>
        </div>
      ) : (
        <>
          {/* OTP Boxes */}
          <div className="space-y-3">
            <div className="flex gap-3 justify-center" onPaste={handlePaste}>
              {otp.map((digit, i) => (
                <input
                  key={i}
                  ref={(el) => (refs.current[i] = el)}
                  type="text"
                  inputMode="numeric"
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleChange(i, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(i, e)}
                  style={{
                    width: "52px", height: "62px",
                    background: digit ? `${DARK.primary}18` : "rgba(255,255,255,0.04)",
                    border: `2px solid ${errors.otp ? DARK.error : digit ? DARK.primary : DARK.border}`,
                    borderRadius: "16px",
                    color: DARK.textPrimary,
                    fontSize: "22px",
                    fontWeight: 700,
                    textAlign: "center",
                    outline: "none",
                    fontFamily: "inherit",
                    boxShadow: digit ? `0 0 0 3px ${DARK.primary}22` : "none",
                    transition: "all 0.18s ease",
                  }}
                  onFocus={(e) => e.target.style.borderColor = DARK.primary}
                  onBlur={(e) => e.target.style.borderColor = digit ? DARK.primary : DARK.border}
                />
              ))}
            </div>
            {errors.otp && (
              <p style={{ color: DARK.error, fontSize: "12px", textAlign: "center" }} className="flex items-center justify-center gap-1">
                <AlertCircle size={12} />{errors.otp}
              </p>
            )}
          </div>

          <PrimaryButton onClick={handleVerify}>Verify & Continue</PrimaryButton>

          <div className="text-center">
            {resent ? (
              <p style={{ color: DARK.primary, fontSize: "13px", fontWeight: 600 }}>✓ Code resent successfully</p>
            ) : (
              <p style={{ color: DARK.textSecondary, fontSize: "13px" }}>
                Didn't receive the code?{" "}
                <button
                  onClick={handleResend}
                  style={{ color: DARK.primary, fontWeight: 700 }}
                  className="hover:underline inline-flex items-center gap-1"
                >
                  <RotateCcw size={12} /> Resend
                </button>
              </p>
            )}
          </div>

          <div className="text-center pt-2">
            <button onClick={onBack} style={{ color: DARK.textSecondary, fontSize: "13px" }} className="hover:underline">
              ← Back to Sign Up
            </button>
          </div>
        </>
      )}
    </div>
  );
}

/* ─────────────────────────────────────────────
   LOGIN VIEW
───────────────────────────────────────────── */
function LoginView({ onSwitch, onOTP }) {
  const [form, setForm] = useState({ identifier: "", password: "" });
  const [showPass, setShowPass] = useState(false);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const set = (k) => (v) => setForm((f) => ({ ...f, [k]: v }));

  const handleLogin = () => {
    const e = {};
    if (!validate.emailOrPhone(form.identifier)) e.identifier = "Enter a valid email or phone number.";
    if (!validate.password(form.password)) e.password = "Password must be at least 6 characters.";
    setErrors(e);
    if (Object.keys(e).length) return;
    setLoading(true);
    setTimeout(() => setLoading(false), 1500);
  };

  return (
    <div className="w-full space-y-5">
      <div>
        <h2 style={{ color: DARK.textPrimary, fontFamily: "'Playfair Display', serif", fontSize: "28px", fontWeight: 700, letterSpacing: "-0.3px" }}>
          Welcome back
        </h2>
        <p style={{ color: DARK.textSecondary, fontSize: "14px", marginTop: "4px" }}>
          Your next adventure is waiting for you.
        </p>
      </div>

      <div className="space-y-4">
        <FloatingInput
          id="login-id" label="Email or Phone Number" value={form.identifier}
          onChange={set("identifier")} error={errors.identifier} icon={Mail}
        />

        <div>
          <div className="flex justify-end mb-1.5">
            <button style={{ color: DARK.primary, fontSize: "12.5px", fontWeight: 600 }} className="hover:underline">
              Forgot Password?
            </button>
          </div>
          <FloatingInput
            id="login-pass" label="Password" type={showPass ? "text" : "password"}
            value={form.password} onChange={set("password")} error={errors.password} icon={Lock}
            rightSlot={
              <button onClick={() => setShowPass(!showPass)} style={{ color: DARK.textSecondary, flexShrink: 0 }}>
                {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            }
          />
        </div>

        <div className="flex gap-2 text-xs justify-center pt-1">
          <button
            style={{ color: DARK.secondary, fontWeight: 600, fontSize: "13px" }}
            className="hover:underline flex items-center gap-1"
          >
            <Sparkles size={12} /> Login with Magic Link
          </button>
          <span style={{ color: DARK.border }}>|</span>
          <button
            onClick={onOTP}
            style={{ color: DARK.secondary, fontWeight: 600, fontSize: "13px" }}
            className="hover:underline flex items-center gap-1"
          >
            <Phone size={12} /> Login via OTP
          </button>
        </div>
      </div>

      <PrimaryButton onClick={handleLogin} loading={loading}>
        Login
      </PrimaryButton>

      <Divider />

      <div className="flex gap-3">
        <OutlineButton icon={Globe}>Continue with Google</OutlineButton>
        <OutlineButton icon={Apple}>Continue with Apple</OutlineButton>
      </div>

      <p style={{ color: DARK.textSecondary, fontSize: "13.5px", textAlign: "center" }}>
        New to Aura?{" "}
        <button onClick={() => onSwitch("signup")} style={{ color: DARK.primary, fontWeight: 700 }} className="hover:underline">
          Sign Up
        </button>
      </p>
    </div>
  );
}

/* ─────────────────────────────────────────────
   SIGN UP VIEW
───────────────────────────────────────────── */
function SignupView({ onSwitch, onOTP }) {
  const [form, setForm] = useState({ name: "", email: "", phone: "", password: "", confirm: "" });
  const [showPass, setShowPass] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [agreed, setAgreed] = useState(false);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const set = (k) => (v) => setForm((f) => ({ ...f, [k]: v }));

  const handleCreate = () => {
    const e = {};
    if (!validate.required(form.name)) e.name = "Full name is required.";
    if (!validate.email(form.email)) e.email = "Enter a valid email address.";
    if (!validate.phone(form.phone)) e.phone = "Enter a valid phone number.";
    if (!validate.password(form.password)) e.password = "Password must be at least 6 characters.";
    if (form.confirm !== form.password) e.confirm = "Passwords must match.";
    if (!agreed) e.agreed = "Please accept the terms to continue.";
    setErrors(e);
    if (Object.keys(e).length) return;
    setLoading(true);
    setTimeout(() => { setLoading(false); onOTP(form.email); }, 1400);
  };

  return (
    <div className="w-full space-y-5">
      <div>
        <h2 style={{ color: DARK.textPrimary, fontFamily: "'Playfair Display', serif", fontSize: "26px", fontWeight: 700, letterSpacing: "-0.3px" }}>
          Create your Aura profile
        </h2>
        <p style={{ color: DARK.textSecondary, fontSize: "14px", marginTop: "4px" }}>
          Join millions exploring the world smarter.
        </p>
      </div>

      <div className="space-y-3.5">
        <FloatingInput id="su-name" label="Full Name" value={form.name} onChange={set("name")} error={errors.name} icon={User} />
        <FloatingInput id="su-email" label="Email Address" value={form.email} onChange={set("email")} error={errors.email} icon={Mail} />
        <FloatingInput id="su-phone" label="Phone Number" value={form.phone} onChange={set("phone")} error={errors.phone} icon={Phone} />
        <FloatingInput
          id="su-pass" label="Password" type={showPass ? "text" : "password"}
          value={form.password} onChange={set("password")} error={errors.password} icon={Lock}
          rightSlot={
            <button onClick={() => setShowPass(!showPass)} style={{ color: DARK.textSecondary }}>
              {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          }
        />
        <FloatingInput
          id="su-confirm" label="Confirm Password" type={showConfirm ? "text" : "password"}
          value={form.confirm} onChange={set("confirm")} error={errors.confirm} icon={Lock}
          rightSlot={
            <button onClick={() => setShowConfirm(!showConfirm)} style={{ color: DARK.textSecondary }}>
              {showConfirm ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          }
        />

        <div className="pt-1">
          <label className="flex items-start gap-3 cursor-pointer">
            <div
              onClick={() => setAgreed(!agreed)}
              style={{
                width: 20, height: 20, borderRadius: 6, flexShrink: 0, marginTop: 1,
                border: `2px solid ${errors.agreed ? DARK.error : agreed ? DARK.primary : DARK.border}`,
                background: agreed ? DARK.primary : "transparent",
                display: "flex", alignItems: "center", justifyContent: "center",
                transition: "all 0.18s",
              }}
            >
              {agreed && <CheckCircle2 size={12} color="#0B132B" strokeWidth={3} />}
            </div>
            <span style={{ color: DARK.textSecondary, fontSize: "13px", lineHeight: 1.5 }}>
              I agree to Aura's{" "}
              <span style={{ color: DARK.primary, fontWeight: 600 }}>Terms & Conditions</span>
              {" "}and{" "}
              <span style={{ color: DARK.primary, fontWeight: 600 }}>Privacy Policy</span>
            </span>
          </label>
          {errors.agreed && (
            <p style={{ color: DARK.error, fontSize: "11.5px", marginLeft: "32px", marginTop: "4px" }} className="flex items-center gap-1">
              <AlertCircle size={11} /> {errors.agreed}
            </p>
          )}
        </div>
      </div>

      <PrimaryButton onClick={handleCreate} loading={loading}>
        Create Account
      </PrimaryButton>

      <Divider />

      <div className="flex gap-3">
        <OutlineButton icon={Globe}>Continue with Google</OutlineButton>
        <OutlineButton icon={Apple}>Continue with Apple</OutlineButton>
      </div>

      <p style={{ color: DARK.textSecondary, fontSize: "13.5px", textAlign: "center" }}>
        Already have an account?{" "}
        <button onClick={() => onSwitch("login")} style={{ color: DARK.primary, fontWeight: 700 }} className="hover:underline">
          Login
        </button>
      </p>
    </div>
  );
}

/* ─────────────────────────────────────────────
   BRAND PANEL (LEFT)
───────────────────────────────────────────── */
function BrandPanel() {
  return (
    <div
      className="hidden md:flex flex-col justify-between p-12 relative overflow-hidden"
      style={{
        background: `linear-gradient(145deg, ${DARK.bg} 0%, #0D1F3C 40%, #0A2342 70%, #061730 100%)`,
        minHeight: "100vh",
        flex: "0 0 45%",
      }}
    >
      {/* Mesh blobs */}
      <div style={{
        position: "absolute", width: 500, height: 500, borderRadius: "50%",
        background: `radial-gradient(circle, ${DARK.primary}20 0%, transparent 70%)`,
        top: -120, left: -120, pointerEvents: "none",
      }} />
      <div style={{
        position: "absolute", width: 400, height: 400, borderRadius: "50%",
        background: `radial-gradient(circle, ${DARK.secondary}18 0%, transparent 70%)`,
        bottom: -80, right: -80, pointerEvents: "none",
      }} />
      <div style={{
        position: "absolute", inset: 0, pointerEvents: "none",
        backgroundImage: `radial-gradient(${DARK.primary}08 1px, transparent 1px)`,
        backgroundSize: "32px 32px",
      }} />

      {/* Logo */}
      <div className="relative z-10">
        <div className="flex items-center gap-3 mb-3">
          <div style={{
            background: `linear-gradient(135deg, ${DARK.primary}, ${DARK.secondary})`,
            borderRadius: "14px", padding: "10px",
            boxShadow: `0 4px 20px ${DARK.primary}44`,
          }}>
            <PlaneTakeoff size={24} color="#0B132B" strokeWidth={2.5} />
          </div>
          <span style={{
            color: DARK.textPrimary,
            fontFamily: "'Playfair Display', serif",
            fontSize: "28px", fontWeight: 700, letterSpacing: "1px",
          }}>
            Aura
          </span>
        </div>
        <p style={{ color: DARK.textSecondary, fontSize: "13px", letterSpacing: "0.06em", fontWeight: 500 }}>
          AI TRAVEL AGENT
        </p>
      </div>

      {/* Main tagline */}
      <div className="relative z-10 space-y-6">
        <h1 style={{
          color: DARK.textPrimary,
          fontFamily: "'Playfair Display', serif",
          fontSize: "clamp(32px, 3.5vw, 48px)",
          fontWeight: 700,
          lineHeight: 1.15,
          letterSpacing: "-0.5px",
        }}>
          Travel at the<br />
          <span style={{
            background: `linear-gradient(90deg, ${DARK.primary}, ${DARK.secondary})`,
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
          }}>
            speed of thought.
          </span>
        </h1>
        <p style={{ color: DARK.textSecondary, fontSize: "15px", lineHeight: 1.7, maxWidth: "320px" }}>
          Your AI travel companion that plans, books, and adapts — so you can focus on the experience, not the logistics.
        </p>

        {/* Feature pills */}
        <div className="flex flex-wrap gap-2 pt-2">
          {["Smart Itineraries", "Real-time Alerts", "Multi-city Trips", "Visa Assistance"].map((tag) => (
            <span key={tag} style={{
              background: `${DARK.primary}18`,
              border: `1px solid ${DARK.primary}33`,
              color: DARK.secondary,
              padding: "5px 12px", borderRadius: "999px",
              fontSize: "12px", fontWeight: 600, letterSpacing: "0.02em",
            }}>
              {tag}
            </span>
          ))}
        </div>
      </div>

      {/* Bottom trust badges */}
      <div className="relative z-10 flex items-center gap-4">
        <div style={{ color: DARK.textSecondary, fontSize: "12px" }} className="flex items-center gap-2">
          <Shield size={14} style={{ color: DARK.primary }} />
          <span>SOC 2 Certified</span>
        </div>
        <div style={{ width: 4, height: 4, borderRadius: "50%", background: DARK.border }} />
        <div style={{ color: DARK.textSecondary, fontSize: "12px" }} className="flex items-center gap-2">
          <Globe size={14} style={{ color: DARK.primary }} />
          <span>190+ Countries</span>
        </div>
        <div style={{ width: 4, height: 4, borderRadius: "50%", background: DARK.border }} />
        <div style={{ color: DARK.textSecondary, fontSize: "12px" }}>
          <span>2M+ Travelers</span>
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────
   ROOT APP
───────────────────────────────────────────── */
export default function AuraAuth() {
  const [view, setView] = useState("login"); // "login" | "signup" | "otp"
  const [otpDest, setOtpDest] = useState("");
  const [animKey, setAnimKey] = useState(0);

  const switchTo = (v, dest = "") => {
    setAnimKey((k) => k + 1);
    setOtpDest(dest);
    setView(v);
  };

  useEffect(() => {
    const link = document.createElement("link");
    link.href = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600;700&display=swap";
    link.rel = "stylesheet";
    document.head.appendChild(link);
  }, []);

  return (
    <div style={{ fontFamily: "'DM Sans', sans-serif", minHeight: "100vh", background: DARK.bg }} className="flex">
      {/* Left Brand Panel */}
      <BrandPanel />

      {/* Right Form Panel */}
      <div
        style={{ background: DARK.surface, flex: 1 }}
        className="flex items-center justify-center min-h-screen px-6 py-12 relative overflow-hidden"
      >
        {/* subtle bg glow */}
        <div style={{
          position: "absolute", width: 600, height: 600, borderRadius: "50%",
          background: `radial-gradient(circle, ${DARK.primary}08 0%, transparent 70%)`,
          top: "50%", left: "50%", transform: "translate(-50%,-50%)",
          pointerEvents: "none",
        }} />

        {/* Mobile logo */}
        <div className="md:hidden absolute top-6 left-6 flex items-center gap-2">
          <div style={{
            background: `linear-gradient(135deg, ${DARK.primary}, ${DARK.secondary})`,
            borderRadius: "10px", padding: "7px",
          }}>
            <PlaneTakeoff size={18} color="#0B132B" strokeWidth={2.5} />
          </div>
          <span style={{ color: DARK.textPrimary, fontFamily: "'Playfair Display', serif", fontSize: "22px", fontWeight: 700 }}>
            Aura
          </span>
        </div>

        <div
          key={animKey}
          style={{
            width: "100%", maxWidth: "420px",
            animation: "fadeSlideIn 0.32s cubic-bezier(0.22,1,0.36,1) both",
          }}
        >
          {view === "login" && (
            <LoginView onSwitch={switchTo} onOTP={() => switchTo("otp", "your phone")} />
          )}
          {view === "signup" && (
            <SignupView onSwitch={switchTo} onOTP={(dest) => switchTo("otp", dest)} />
          )}
          {view === "otp" && (
            <OTPView onBack={() => switchTo("signup")} destination={otpDest} />
          )}
        </div>
      </div>

      <style>{`
        @keyframes fadeSlideIn {
          from { opacity: 0; transform: translateY(18px) scale(0.98); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }
        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus {
          -webkit-box-shadow: 0 0 0 1000px ${DARK.surface} inset !important;
          -webkit-text-fill-color: ${DARK.textPrimary} !important;
        }
        * { box-sizing: border-box; }
        input, button { font-family: 'DM Sans', sans-serif; }
        ::-webkit-scrollbar { display: none; }
      `}</style>
    </div>
  );
}
