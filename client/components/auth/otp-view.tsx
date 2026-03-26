/*"use client";
import { useState, useRef } from "react";
import { Shield, RotateCcw, CheckCircle2 } from "lucide-react";
import { PrimaryButton } from "./ui-elements";
import { DARK_THEME } from "@/lib/auth-utils";

export default function OTPView({ onBack, destination, onSuccess }: any) {
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [verified, setVerified] = useState(false);
  
  // 1. Explicitly type the ref as an array of Inputs
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  const handleChange = (index: number, val: string) => {
    if (!/^\d?$/.test(val)) return;
    const next = [...otp];
    next[index] = val;
    setOtp(next);
    
    // 2. Move focus to next input if value exists
    if (val && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    // 3. Move focus back on Backspace
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleVerify = () => {
    if (otp.join("").length === 6) {
      setVerified(true);
      setTimeout(() => onSuccess?.(), 1500);
    }
  };

  return (
    <div className="space-y-8 text-center">
      {!verified ? (
        <>
          <header className="flex flex-col items-center">
            <div className="p-3 rounded-2xl mb-4" style={{ background: `${DARK_THEME.primary}22` }}>
              <Shield size={32} className="text-cyan-400" />
            </div>
            <h2 className="text-2xl font-bold text-white font-serif">Verify device</h2>
            <p className="text-sm text-slate-400 mt-2">Code sent to <span className="text-cyan-400 font-bold">{destination}</span></p>
          </header>

          <div className="flex gap-2 justify-center">
            {otp.map((digit, i) => (
              <input
                key={i}
                // 4. THE FIX: Explicitly set the ref without returning the assignment
                ref={(el) => {
                  inputRefs.current[i] = el;
                }}
                type="text"
                inputMode="numeric"
                maxLength={1}
                value={digit}
                onKeyDown={(e) => handleKeyDown(i, e)}
                onChange={(e) => handleChange(i, e.target.value)}
                style={{ 
                  background: digit ? `${DARK_THEME.primary}15` : "rgba(255,255,255,0.04)", 
                  borderColor: digit ? DARK_THEME.primary : DARK_THEME.border 
                }}
                className="w-12 h-16 rounded-xl border-2 text-2xl font-bold text-white text-center outline-none focus:border-cyan-400 transition-all"
              />
            ))}
          </div>

          <PrimaryButton onClick={handleVerify}>Verify & Enter</PrimaryButton>

          <button onClick={onBack} className="text-xs text-slate-500 flex items-center gap-2 mx-auto hover:text-white transition-colors">
            <RotateCcw size={12} /> Change email
          </button>
        </>
      ) : (
        <div className="py-10 animate-in zoom-in-95 duration-300">
          <div className="w-20 h-20 rounded-full bg-cyan-500/20 flex items-center justify-center mx-auto mb-6">
            <CheckCircle2 size={40} className="text-cyan-400" />
          </div>
          <h2 className="text-2xl font-bold text-white">Access Granted</h2>
        </div>
      )}
    </div>
  );
}*/
/*"use client";
import { useState, useRef } from "react";
import { PrimaryButton } from "./ui-elements";

export default function OTPView({ destination, onSuccess }: any) {
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  const handleVerify = async () => {
    if (otp.join("").length === 6) {
      const res = await fetch("http://localhost:8000/api/verify", { method: "POST" });
      if (res.ok) onSuccess();
    }
  };

  return (
    <div className="space-y-6 text-center">
      <h2 className="text-2xl font-bold font-serif">Verify Device</h2>
      <p className="text-slate-400 text-sm">Sent to {destination}</p>
      <div className="flex gap-2 justify-center">
        {otp.map((digit, i) => (
          <input
            key={i} 
            ref={(el) => { inputRefs.current[i] = el; }}
            className="w-12 h-14 rounded-xl bg-white/5 border border-white/10 text-center text-xl font-bold"
            maxLength={1}
            value={digit}
            onChange={(e) => {
                const next = [...otp]; next[i] = e.target.value; setOtp(next);
                if (e.target.value && i < 5) inputRefs.current[i+1]?.focus();
            }}
          />
        ))}
      </div>
      <PrimaryButton onClick={handleVerify}>Verify & Continue</PrimaryButton>
    </div>
  );
}*/
/*"use client";
import { useState, useRef } from "react";
import { PrimaryButton } from "./ui-elements";

export default function OTPView({ destination, onSuccess }: any) {
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

 const handleVerify = async () => {
  try {
    const res = await fetch("http://localhost:8000/api/verify", { 
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    if (res.ok) {
      setVerified(true);
      // Give the "Success" animation a moment to breathe
      setTimeout(() => {
        if (onSuccess) {
            onSuccess(); // This calls router.push("/dashboard")
        } else {
            console.error("onSuccess prop is missing!");
        }
      }, 1500);
    }
  } catch (error) {
    console.error("Redirection failed:", error);
  }
};

  return (
    <div className="space-y-8 text-center">
      <h2 className="text-2xl font-bold text-white font-serif">Verify Identity</h2>
      <div className="flex gap-2 justify-center">
        {otp.map((digit, i) => (
          <input
            key={i} ref={(el) => { inputRefs.current[i] = el; }}
            className="w-12 h-16 rounded-xl bg-white/5 border border-white/10 text-center text-2xl font-bold"
            maxLength={1} value={digit}
            onChange={(e) => {
                const next = [...otp]; next[i] = e.target.value; setOtp(next);
                if (e.target.value && i < 5) inputRefs.current[i+1]?.focus();
            }}
          />
        ))}
      </div>
      <PrimaryButton onClick={handleVerify}>Verify & Continue</PrimaryButton>
    </div>
  );
}*/
/*"use client";
import { useState, useRef } from "react";
import { CheckCircle2, ShieldCheck, Loader2 } from "lucide-react"; // Added for visual impact
import { PrimaryButton } from "./ui-elements";

export default function OTPView({ destination, onSuccess }: any) {
  // 1. THIS IS THE MISSING PIECE: Define the verified state
  const [verified, setVerified] = useState(false);
  const [loading, setLoading] = useState(false);
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  const handleVerify = async () => {
    if (otp.join("").length < 6) return;
    
    setLoading(true);
    try {
      // 2. Talk to the FastAPI brain
      const res = await fetch("http://localhost:8000/api/verify", { 
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });

      if (res.ok) {
        setVerified(true); // Now this works!
        // 3. Natural delay for the success animation
        setTimeout(() => {
          onSuccess(); 
        }, 1500);
      }
    } catch (error) {
      console.error("Connection error:", error);
    } finally {
      setLoading(false);
    }
  };

  // 4. THE UI: Switch between the Input and the "Success" screen
  if (verified) {
    return (
      <div className="flex flex-col items-center justify-center space-y-4 py-10 animate-in zoom-in-95 duration-500">
        <div className="w-20 h-20 rounded-full bg-cyan-500/20 flex items-center justify-center">
          <CheckCircle2 size={40} className="text-cyan-400" />
        </div>
        <h2 className="text-2xl font-bold text-white font-serif">Identity Verified</h2>
        <p className="text-slate-400 text-sm">Preparing your AURA environment...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 text-center animate-in fade-in duration-500">
      <header className="space-y-2">
        <div className="mx-auto w-12 h-12 bg-cyan-500/10 rounded-xl flex items-center justify-center mb-4">
          <ShieldCheck size={24} className="text-cyan-400" />
        </div>
        <h2 className="text-2xl font-bold text-white font-serif">Verify Device</h2>
        <p className="text-slate-400 text-xs">Sent to <span className="text-cyan-400">{destination || "your email"}</span></p>
      </header>

      <div className="flex gap-2 justify-center">
        {otp.map((digit, i) => (
          <input
            key={i}
            ref={(el) => { inputRefs.current[i] = el; }}
            type="text"
            maxLength={1}
            value={digit}
            onChange={(e) => {
              const val = e.target.value;
              if (!/^\d?$/.test(val)) return;
              const next = [...otp];
              next[i] = val;
              setOtp(next);
              if (val && i < 5) inputRefs.current[i + 1]?.focus();
            }}
            onKeyDown={(e) => {
              if (e.key === "Backspace" && !otp[i] && i > 0) inputRefs.current[i - 1]?.focus();
            }}
            className="w-12 h-16 rounded-xl bg-white/5 border border-white/10 text-center text-2xl font-bold text-white focus:border-cyan-400 outline-none transition-all"
          />
        ))}
      </div>

      <PrimaryButton onClick={handleVerify} loading={loading}>
        {loading ? "Verifying..." : "Verify & Continue"}
      </PrimaryButton>
    </div>
  );
}*/
/*"use client";
import { useState, useRef } from "react";
import { CheckCircle2, ShieldCheck, Loader2 } from "lucide-react"; // Added for visual impact
import { PrimaryButton } from "./ui-elements";

export default function OTPView({ destination, onSuccess }: any) {
  // 1. THIS IS THE MISSING PIECE: Define the verified state
  const [verified, setVerified] = useState(false);
  const [loading, setLoading] = useState(false);
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  const handleVerify = async () => {
    if (otp.join("").length < 6) return;
    
    setLoading(true);
    try {
      // 2. Talk to the FastAPI brain
      const res = await fetch("http://localhost:8000/api/verify", { 
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });

      if (res.ok) {
        setVerified(true); // Now this works!
        // 3. Natural delay for the success animation
        setTimeout(() => {
          onSuccess(); 
        }, 1500);
      }
    } catch (error) {
      console.error("Connection error:", error);
    } finally {
      setLoading(false);
    }
  };

  // 4. THE UI: Switch between the Input and the "Success" screen
  if (verified) {
    return (
      <div className="flex flex-col items-center justify-center space-y-4 py-10 animate-in zoom-in-95 duration-500">
        <div className="w-20 h-20 rounded-full bg-cyan-500/20 flex items-center justify-center">
          <CheckCircle2 size={40} className="text-cyan-400" />
        </div>
        <h2 className="text-2xl font-bold text-white font-serif">Identity Verified</h2>
        <p className="text-slate-400 text-sm">Preparing your AURA environment...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8 text-center animate-in fade-in duration-500">
      <header className="space-y-2">
        <div className="mx-auto w-12 h-12 bg-cyan-500/10 rounded-xl flex items-center justify-center mb-4">
          <ShieldCheck size={24} className="text-cyan-400" />
        </div>
        <h2 className="text-2xl font-bold text-white font-serif">Verify Device</h2>
        <p className="text-slate-400 text-xs">Sent to <span className="text-cyan-400">{destination || "your email"}</span></p>
      </header>

      <div className="flex gap-2 justify-center">
        {otp.map((digit, i) => (
          <input
            key={i}
            ref={(el) => { inputRefs.current[i] = el; }}
            type="text"
            maxLength={1}
            value={digit}
            onChange={(e) => {
              const val = e.target.value;
              if (!/^\d?$/.test(val)) return;
              const next = [...otp];
              next[i] = val;
              setOtp(next);
              if (val && i < 5) inputRefs.current[i + 1]?.focus();
            }}
            onKeyDown={(e) => {
              if (e.key === "Backspace" && !otp[i] && i > 0) inputRefs.current[i - 1]?.focus();
            }}
            className="w-12 h-16 rounded-xl bg-white/5 border border-white/10 text-center text-2xl font-bold text-white focus:border-cyan-400 outline-none transition-all"
          />
        ))}
      </div>

      <PrimaryButton onClick={handleVerify} loading={loading}>
        {loading ? "Verifying..." : "Verify & Continue"}
      </PrimaryButton>
    </div>
  );
}*/

/*"use client";
import { useState, useRef } from "react";
import { useRouter } from "next/navigation"; // Backup redirect
import { CheckCircle2, Loader2 } from "lucide-react";
import { PrimaryButton } from "./ui-elements";

export default function OTPView({ destination, onSuccess }: any) {
  const [verified, setVerified] = useState(false);
  const [loading, setLoading] = useState(false);
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const router = useRouter();
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

 /* const handleVerify = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/verify", { method: "POST" });
      
      if (res.ok) {
        setVerified(true);
        setTimeout(() => {
          // Try the prop first, then the direct router
          if (onSuccess) onSuccess();
          else router.push("/dashboard");
        }, 1500);
      }
    } catch (e) {
      console.error("Verify Failed", e);
    } finally {
      setLoading(false);
    }
  };

  if (verified) return (
    <div className="text-center py-10 animate-pulse">
      <CheckCircle2 size={60} className="text-cyan-400 mx-auto mb-4" />
      <h2 className="text-2xl font-bold">Access Granted</h2>
    </div>
  );

const handleVerify = async () => {
  setLoading(true);
  try {
    const res = await fetch("http://localhost:8000/api/verify", { 
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    
    if (res.ok) {
      setVerified(true);
      
      // 🚀 THE HACKATHON HAMMER: Force a hard redirect
      setTimeout(() => {
        window.location.href = "/dashboard"; 
      }, 1200);
      
    } else {
      console.error("Backend rejected verification");
    }
  } catch (e) {
    console.error("Verify Failed", e);
  } finally {
    setLoading(false);
  }
};
  return (
    <div className="space-y-6 text-center">
      <h2 className="text-2xl font-bold font-serif">Verify Identity</h2>
      <div className="flex gap-2 justify-center">
        {otp.map((digit, i) => (
          <input
            key={i} ref={(el) => { inputRefs.current[i] = el; }}
            className="w-12 h-16 rounded-xl bg-white/5 border border-white/10 text-center text-2xl font-bold"
            maxLength={1} value={digit}
            onChange={(e) => {
                const next = [...otp]; next[i] = e.target.value; setOtp(next);
                if (e.target.value && i < 5) inputRefs.current[i+1]?.focus();
            }}
          />
        ))}
      </div>
      <PrimaryButton onClick={handleVerify} loading={loading}>
        {loading ? "Authorizing..." : "Verify & Continue"}
      </PrimaryButton>
    </div>
  );
}*/
"use client";
import { useState, useRef } from "react";
import { CheckCircle2, ShieldCheck } from "lucide-react";
import { PrimaryButton } from "./ui-elements";

export default function OTPView({ destination, onSuccess }: any) {
  const [verified, setVerified] = useState(false);
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  const handleVerify = async () => {
    if (otp.join("").length < 6) return;
    
    const res = await fetch("http://localhost:8000/api/verify", { method: "POST" });
    if (res.ok) {
      setVerified(true);
      setTimeout(() => {
        onSuccess(); // 🚀 Triggers window.location.href = "/dashboard"
      }, 1200);
    }
  };

  if (verified) return (
    <div className="text-center space-y-4 animate-in zoom-in duration-500">
      <CheckCircle2 size={64} className="text-cyan-400 mx-auto" />
      <h2 className="text-2xl font-bold">Identity Verified</h2>
      <p className="text-slate-400">Welcome to the future of travel.</p>
    </div>
  );

  return (
    <div className="space-y-8 text-center animate-in slide-in-from-bottom-4 duration-500">
      <div className="mx-auto w-12 h-12 bg-cyan-500/10 rounded-xl flex items-center justify-center">
        <ShieldCheck className="text-cyan-400" />
      </div>
      <h2 className="text-2xl font-bold font-serif">Enter OTP</h2>
      <div className="flex gap-2 justify-center">
        {otp.map((digit, i) => (
          <input
            key={i} ref={(el) => { inputRefs.current[i] = el; }}
            className="w-12 h-16 rounded-xl bg-white/5 border border-white/10 text-center text-2xl font-bold text-white"
            maxLength={1} value={digit}
            onChange={(e) => {
                const next = [...otp]; next[i] = e.target.value; setOtp(next);
                if (e.target.value && i < 5) inputRefs.current[i+1]?.focus();
            }}
          />
        ))}
      </div>
      <PrimaryButton onClick={handleVerify}>Verify & Continue</PrimaryButton>
    </div>
  );
}