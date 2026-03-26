"use client";
import { useState } from "react";
import { Mail, Lock, Eye, EyeOff, Globe, Apple } from "lucide-react";
import { FloatingInput, PrimaryButton } from "./ui-elements";
import { validate, DARK_THEME } from "@/lib/auth-utils";

export default function LoginForm({ onSwitch, onOTP }: any) {
  const [form, setForm] = useState({ identifier: "", password: "" });
  const [showPass, setShowPass] = useState(false);
  const [errors, setErrors] = useState<any>({});
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    // 1. Clear old errors
    const e: any = {};
    if (!validate.emailOrPhone(form.identifier)) e.identifier = "Enter a valid email or phone.";
    if (!validate.password(form.password)) e.password = "Password too short.";
    setErrors(e);
    
    // 2. Stop if there are errors
    if (Object.keys(e).length > 0) return;

    setLoading(true);

    try {
        // 3. Talk to your FastAPI server
        const res = await fetch("http://localhost:8000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ 
                identifier: form.identifier, 
                password: form.password 
            }),
        });

        if (res.ok) {
            // SUCCESS: This triggers the view change in your AuthPage (page.tsx)
            onOTP(); 
        } else {
            setErrors({ identifier: "User not found or wrong password." });
        }
    } catch (err) {
        setErrors({ identifier: "AURA Brain is offline. Run your FastAPI server!" });
    } finally {
        setLoading(false);
    }
};

  return (
    <div className="space-y-6">
      <header>
        <h2 className="text-3xl font-bold text-white font-serif">Welcome back</h2>
        <p className="text-sm text-slate-400 mt-2">Sign in to resume your journey.</p>
      </header>

      <div className="space-y-4">
        <FloatingInput 
          label="Email or Phone" icon={Mail} value={form.identifier} 
          onChange={(v: string) => setForm({...form, identifier: v})} error={errors.identifier} 
        />
        <FloatingInput 
          label="Password" type={showPass ? "text" : "password"} icon={Lock} value={form.password} 
          onChange={(v: string) => setForm({...form, password: v})} error={errors.password}
          rightSlot={<button onClick={() => setShowPass(!showPass)}>{showPass ? <EyeOff size={16}/> : <Eye size={16}/>}</button>}
        />
      </div>

      <PrimaryButton onClick={handleLogin} loading={loading}>Sign In</PrimaryButton>

      <p className="text-center text-sm text-slate-500">
        New to Aura? <button onClick={onSwitch} className="text-cyan-500 font-bold hover:underline">Create Account</button>
      </p>
    </div>
  );
}