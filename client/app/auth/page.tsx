/*"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import BrandPanel from "@/components/auth/brand-panel";
import LoginView from "@/components/auth/login-form";
import SignupView from "@/components/auth/signup-form";
import OTPView from "@/components/auth/otp-view";
import { DARK_THEME } from "@/lib/auth-utils";

export default function AuthPage() {
  const [view, setView] = useState<"login" | "signup" | "otp">("login");
  const [otpDest, setOtpDest] = useState("");
  const router = useRouter();

  // This handles the final redirect after OTP is verified
  const handleAuthSuccess = () => {
    router.push("/dashboard"); 
  };

  return (
    <div style={{ backgroundColor: DARK_THEME.bg }} className="flex min-h-screen font-sans selection:bg-cyan-500/30">
      {/* Left Side: Visuals 
    }
      <BrandPanel />
      
      {/* Right Side: Logic }
      <main style={{ backgroundColor: DARK_THEME.surface }} className="flex-1 flex items-center justify-center p-6 relative">
        <div className="w-full max-w-[420px] animate-in fade-in slide-in-from-bottom-4 duration-500">
          {view === "login" && (
            <LoginView 
              onSwitch={() => setView("signup")} 
              onOTP={() => setView("otp")} 
            />
          )}
          {view === "signup" && (
            <SignupView 
              onSwitch={() => setView("login")} 
              onOTP={(dest: string) => { setOtpDest(dest); setView("otp"); }} 
            />
          )}
          {view === "otp" && (
            <OTPView 
              onBack={() => setView("signup")} 
              destination={otpDest} 
              onSuccess={handleAuthSuccess} 
            />
          )}
        </div>
      </main>
    </div>
  );
}*/
/*"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import BrandPanel from "@/components/auth/brand-panel";
import LoginView from "@/components/auth/login-form";
import SignupView from "@/components/auth/signup-form";
import OTPView from "@/components/auth/otp-view";
import { DARK_THEME } from "@/lib/auth-utils";

export default function AuthPage() {
  const [view, setView] = useState<"login" | "signup" | "otp">("login");
  const [email, setEmail] = useState("");
  const router = useRouter();

  const handleAuthSuccess = () => {
  console.log("Auth Success! Redirecting...");
  router.push("/dashboard"); 
};

  return (
    <div style={{ backgroundColor: DARK_THEME.bg }} className="flex min-h-screen text-white">
      <BrandPanel />
      <main className="flex-1 flex items-center justify-center p-6 bg-[#1C2541]">
        <div className="w-full max-w-[400px]">
          {view === "login" && <LoginView onSwitch={() => setView("signup")} onOTP={() => setView("otp")} />}
          {view === "signup" && <SignupView onSwitch={() => setView("login")} onOTP={(e:string) => {setEmail(e); setView("otp")}} />}
          {view === "otp" && (
  <OTPView 
    destination={email} 
    onSuccess={handleAuthSuccess} // <--- THIS MUST BE HERE
  />
)}
        </div>
      </main>
    </div>
  );
}*/
/*"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation"; // Ensure it's next/navigation
import BrandPanel from "@/components/auth/brand-panel";
import LoginView from "@/components/auth/login-form";
import SignupView from "@/components/auth/signup-form";
import OTPView from "@/components/auth/otp-view";
import { DARK_THEME } from "@/lib/auth-utils";

export default function AuthPage() {
  const [view, setView] = useState<"login" | "signup" | "otp">("login");
  const [email, setEmail] = useState("");
  const router = useRouter();

  const handleAuthSuccess = () => {
    console.log("🚀 REDIRECTING TO DASHBOARD...");
    router.push("/dashboard"); 
  };

  return (
    <div style={{ backgroundColor: DARK_THEME.bg }} className="flex min-h-screen text-white">
      <BrandPanel />
      <main className="flex-1 flex items-center justify-center p-6 bg-[#0B132B]">
        <div className="w-full max-w-[400px]">
          {view === "login" && (
            <LoginView onSwitch={() => setView("signup")} onOTP={() => setView("otp")} />
          )}
          {view === "signup" && (
            <SignupView 
              onSwitch={() => setView("login")} 
              onOTP={(e: string) => {
                setEmail(e);
                setView("otp");
              }} 
            />
          )}
          {view === "otp" && (
            <OTPView 
              destination={email} 
              onSuccess={handleAuthSuccess} 
            />
          )}
        </div>
      </main>
    </div>
  );
}*/
"use client";
import { useState } from "react";
import BrandPanel from "@/components/auth/brand-panel";
import LoginView from "@/components/auth/login-form";
import SignupView from "@/components/auth/signup-form";
import OTPView from "@/components/auth/otp-view";

export default function AuthPage() {
  const [view, setView] = useState<"login" | "signup" | "otp">("login");
  const [email, setEmail] = useState("");

  const handleGoToDashboard = () => {
    console.log("🚀 Launching Dashboard...");
    window.location.href = "/dashboard"; // Hard redirect to clear cache
  };

  return (
    <div className="flex min-h-screen bg-[#0B132B] text-white">
      <BrandPanel />
      <main className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-[400px]">
          {view === "login" && (
            <LoginView onSwitch={() => setView("signup")} onOTP={() => setView("otp")} />
          )}
          
          {view === "signup" && (
            <SignupView 
              onSwitch={() => setView("login")} 
              onOTP={(e: string) => {
                setEmail(e);
                setView("otp"); // 🚀 Moves forward to OTP
              }} 
            />
          )}

          {view === "otp" && (
            <OTPView 
                destination={email} 
                onSuccess={handleGoToDashboard} 
            />
          )}
        </div>
      </main>
    </div>
  );
}