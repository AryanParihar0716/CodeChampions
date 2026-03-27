/*"use client";
import { useState } from "react";
import { User, Mail, Phone, Lock, Eye, EyeOff, CheckCircle2, Globe, Apple } from "lucide-react";
import { FloatingInput, PrimaryButton } from "./ui-elements";
import { validate, DARK_THEME } from "@/lib/auth-utils";

export default function SignupView({ onSwitch, onOTP }: any) {
  const [form, setForm] = useState({ name: "", email: "", phone: "", password: "", confirm: "" });
  const [showPass, setShowPass] = useState(false);
  const [agreed, setAgreed] = useState(false);
  const [errors, setErrors] = useState<any>({});
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    const e: any = {};
    if (!validate.required(form.name)) e.name = "Full name is required.";
    if (!validate.email(form.email)) e.email = "Invalid email address.";
    if (!validate.phone(form.phone)) e.phone = "Invalid phone number.";
    if (!validate.password(form.password)) e.password = "Minimum 6 characters.";
    if (form.confirm !== form.password) e.confirm = "Passwords do not match.";
    if (!agreed) e.agreed = "You must agree to terms.";
    setErrors(e);

    if (Object.keys(e).length === 0) {
      setLoading(true);
      // Simulate API registration call
      setTimeout(() => {
        setLoading(false);
        onOTP(form.email); // Move to OTP and show the email as destination
      }, 1500);
    }
  };

  return (
    <div className="space-y-5">
      <header>
        <h2 className="text-2xl font-bold text-white font-serif">Create your Aura profile</h2>
        <p className="text-sm text-slate-400 mt-2">Join millions exploring the world smarter.</p>
      </header>

      <div className="space-y-3">
        <FloatingInput label="Full Name" icon={User} value={form.name} onChange={(v:any) => setForm({...form, name: v})} error={errors.name} />
        <FloatingInput label="Email Address" icon={Mail} value={form.email} onChange={(v:any) => setForm({...form, email: v})} error={errors.email} />
        <FloatingInput label="Phone Number" icon={Phone} value={form.phone} onChange={(v:any) => setForm({...form, phone: v})} error={errors.phone} />
        <FloatingInput 
          label="Password" type={showPass ? "text" : "password"} icon={Lock} value={form.password} 
          onChange={(v:any) => setForm({...form, password: v})} error={errors.password}
          rightSlot={<button onClick={() => setShowPass(!showPass)}>{showPass ? <EyeOff size={16}/> : <Eye size={16}/>}</button>}
        />
      </div>

      <div className="flex items-start gap-3 px-1 py-2">
        <div 
          onClick={() => setAgreed(!agreed)}
          style={{ background: agreed ? DARK_THEME.primary : "transparent", borderColor: errors.agreed ? DARK_THEME.error : DARK_THEME.border }}
          className="w-5 h-5 rounded-md border-2 flex items-center justify-center cursor-pointer transition-all"
        >
          {agreed && <CheckCircle2 size={12} color="#0B132B" strokeWidth={3} />}
        </div>
        <p className="text-xs text-slate-500 leading-tight">
          I agree to Aura's <span className="text-cyan-500 font-semibold cursor-pointer">Terms</span> and <span className="text-cyan-500 font-semibold cursor-pointer">Privacy Policy</span>.
        </p>
      </div>

      <PrimaryButton onClick={handleCreate} loading={loading}>Create Account</PrimaryButton>

      <p className="text-center text-sm text-slate-500">
        Already have an account? <button onClick={onSwitch} className="text-cyan-500 font-bold hover:underline">Login</button>
      </p>
    </div>
  );
}*/
/*"use client";
import { useState } from "react";
import { FloatingInput, PrimaryButton } from "./ui-elements";

export default function SignupView({ onSwitch, onOTP }: any) {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    setLoading(true);
    try {
        const res = await fetch("http://localhost:8000/api/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(form),
        });
        if (res.ok) onOTP(form.email); // Go to OTP screen
    } catch (err) {
        console.error("Signup failed");
    } finally { setLoading(false); }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold font-serif text-white">Join AURA</h2>
      <div className="space-y-4">
        <FloatingInput label="Full Name" value={form.name} onChange={(v:string) => setForm({...form, name:v})} />
        <FloatingInput label="Email" value={form.email} onChange={(v:string) => setForm({...form, email:v})} />
        <FloatingInput label="Password" type="password" value={form.password} onChange={(v:string) => setForm({...form, password:v})} />
      </div>
      <PrimaryButton onClick={handleCreate} loading={loading}>Create Account</PrimaryButton>
    </div>
  );
}*/
/*"use client";
import { useState } from "react";
import { FloatingInput, PrimaryButton } from "./ui-elements";

export default function SignupView({ onSwitch, onOTP }: any) {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);

 // Inside your SignupForm component
const handleCreate = async (e: React.FormEvent) => {
  e.preventDefault();
  setLoading(true);

  try {
    const response = await fetch("http://127.0.0.1:8000/api/signup", { // 🚀 Use 127.0.0.1 instead of localhost
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      }),
    });

    if (response.ok) {
      // Logic for moving to OTP view
      setStep("otp"); 
    } else {
      const errorData = await response.json();
      alert(errorData.detail || "Signup failed");
    }
  } catch (error) {
    console.error("Signup Error:", error);
    alert("Backend Server is Offline. Make sure your FastAPI server is running on port 8000.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <h2 className="text-3xl font-bold font-serif">Join AURA</h2>
      <div className="space-y-4">
        <FloatingInput label="Full Name" value={form.name} onChange={(v:string) => setForm({...form, name:v})} />
        <FloatingInput label="Email Address" value={form.email} onChange={(v:string) => setForm({...form, email:v})} />
        <FloatingInput label="Password" type="password" value={form.password} onChange={(v:string) => setForm({...form, password:v})} />
      </div>
      <PrimaryButton onClick={handleCreate} loading={loading}>Create Account</PrimaryButton>
      <button onClick={onSwitch} className="text-sm text-slate-500 hover:text-cyan-400 w-full text-center">
        Already a traveler? Sign In
      </button>
    </div>
  );
}*/
"use client";
import { useState } from "react";
import { FloatingInput, PrimaryButton } from "./ui-elements";

export default function SignupView({ onSwitch, onOTP }: any) {
  // 🚀 Your state is called 'form'
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    setLoading(true);

    try {
      // 🚀 Using 127.0.0.1 is the safest bet for Windows/FastAPI
      const response = await fetch("http://127.0.0.1:8000/api/signup", { 
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: form.name,      // ✅ Fixed: was formData.name
          email: form.email,    // ✅ Fixed: was formData.email
          password: form.password, // ✅ Fixed: was formData.password
        }),
      });

      if (response.ok) {
        // 🚀 Move to the OTP screen using the prop passed from auth/page.tsx
        onOTP(form.email); 
      } else {
        const errorData = await response.json();
        alert(errorData.detail || "Signup failed");
      }
    } catch (error) {
      console.error("Signup Error:", error);
      alert("Backend Offline. Check if your FastAPI terminal shows 'Uvicorn running'.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <header>
        <h2 className="text-3xl font-bold font-serif">Join AURA</h2>
        <p className="text-xs text-slate-500 mt-1 font-mono uppercase tracking-widest">Initialization Phase // 01</p>
      </header>
      
      <div className="space-y-4">
        <FloatingInput label="Full Name" value={form.name} onChange={(v:string) => setForm({...form, name:v})} />
        <FloatingInput label="Email Address" value={form.email} onChange={(v:string) => setForm({...form, email:v})} />
        <FloatingInput label="Password" type="password" value={form.password} onChange={(v:string) => setForm({...form, password:v})} />
      </div>

      <PrimaryButton onClick={handleCreate} loading={loading}>Create Account</PrimaryButton>
      
      <button onClick={onSwitch} className="text-sm text-slate-500 hover:text-cyan-400 w-full text-center transition-colors">
        Already a traveler? <span className="text-cyan-500 font-bold">Sign In</span>
      </button>
    </div>
  );
}