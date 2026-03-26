"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow your Next.js app to talk to this
    allow_methods=["*"],
    allow_headers=["*"],
)


# Simple Agentic Logic
def visa_check_node(state: dict):
    dest = state.get("destination", "").lower()
    # Mock Logic: Indian passport context
    e_visa = ['Argentina', 'Armenia', 'Azerbaijan', 'Bahrain', 'Benin', 'Colombia', 'Cote D\'Ivoire', 'Djibouti', 'Georgia', 'Kazakhstan', 'Kyrgyzstan Republic', 'Lesotho', 'Malaysia', 'Moldova', 'New Zealand', 'Oman', 'Papua New Guinea', 'Russian Federation', 'Singapore', 'South Korea', 'Taiwan', 'Turkey', 'Uganda', 'Uzbekistan', 'Zambia']
    visa_free = ['Barbados', 'Bhutan', 'Dominica', 'Grenada', 'Haiti', 'Hong Kong', 'Maldives', 'Mauritius', 'Montserrat', 'Nepal', 'Niue Island', 'Saint Vincent & the Grenadines', 'Samoa', 'Senegal', 'Serbia', 'Trinidad & Tobago']
    Visa_on_arrival = [
    'Angola', 'Bolivia', 'Cabo Verde', 'Cameroon', 'Cook Islands', 'Fiji', 'Guinea Bissau',
    'Indonesia', 'Iran', 'Jamaica', 'Jordan', 'Kiribati', 'Laos', 'Madagascar', 'Mauritania',
    'Nigeria', 'Qatar', 'Republic of Marshall Islands', 'Reunion Island', 'Rwanda', 'Seychelles',
    'Somalia', 'Tunisia', 'Tuvalu', 'Vanuatu', 'Zimbabwe'
    ]

    VoA_Evisa = [
    'Kenya', 'Myanmar', 'Saint Lucia', 'Sri Lanka', 'Suriname', 'Tajikistan', 'Tanzania',
    'Thailand', 'Vietnam', 'Ethiopia', 'Cambodia'
    ]
    if dest in e_visa:
        visa = "e-Visa"
    elif dest in visa_free:
        visa = "Visa-Free"
    elif dest in Visa_on_arrival:
        visa = "Visa on Arrival"
    elif dest in VoA_Evisa:
        visa = "Visa on Arrival or e-Visa"
    else:
        visa = "Visa Required"
    return {"visa_status": visa}

workflow = StateGraph(dict)
workflow.add_node("check_visa", visa_check_node)
workflow.add_edge(START, "check_visa")
workflow.add_edge("check_visa", END)
agent = workflow.compile()

@app.post("/api/chat")
async def chat(data: dict):
    response = agent.invoke({"destination": data.get("message", "Thailand")})
    return {
        "reply": f"Thinking about {data.get('message')}? Great choice! Here is the agentic breakdown:",
        "visa": response["visa_status"]
    }"""
"""from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from typing import Dict, Optional

app = FastAPI()

# ─────────────────────────────────────────────
# MIDDLEWARE (CORS)
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Specifically allow your Next.js app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# DATABASE (MOCK FOR HACKATHON)
# ─────────────────────────────────────────────
# In a real app, you'd use SQLAlchemy + PostgreSQL
users_db: Dict[str, dict] = {}

# ─────────────────────────────────────────────
# AUTH MODELS & LOGIC
# ─────────────────────────────────────────────
class UserSignup(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    identifier: str # Email or Phone
    password: str

@app.post("/api/signup")
async def signup(user: UserSignup):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Store user data
    users_db[user.email] = {
        "name": user.name,
        "password": user.password, # Note: In production, always hash passwords!
        "phone": user.phone
    }
    return {"message": f"OTP sent to {user.email}"}

@app.post("/api/login")
async def login(user: UserLogin):
    # Check if user exists and password matches
    user_data = users_db.get(user.identifier)
    if not user_data or user_data["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}

@app.post("/api/verify")
async def verify(data: dict, response: Response):
    # For the hackathon, we accept any 6-digit OTP
    # We set a cookie so the Frontend Middleware lets the user into the /dashboard
    response.set_cookie(
        key="aura_token", 
        value="aura_session_active", 
        httponly=False, # Set to False so client-side JS can see it if needed
        max_age=3600    # 1 hour session
    )
    return {"status": "verified"}

# ─────────────────────────────────────────────
# LANGGRAPH AGENTIC LOGIC (Your Original Logic)
# ─────────────────────────────────────────────
def visa_check_node(state: dict):
    dest = state.get("destination", "").lower().capitalize()
    
    e_visa = ['Argentina', 'Armenia', 'Azerbaijan', 'Bahrain', 'Benin', 'Colombia', "Cote D'Ivoire", 'Djibouti', 'Georgia', 'Kazakhstan', 'Kyrgyzstan Republic', 'Lesotho', 'Malaysia', 'Moldova', 'New Zealand', 'Oman', 'Papua New Guinea', 'Russian Federation', 'Singapore', 'South Korea', 'Taiwan', 'Turkey', 'Uganda', 'Uzbekistan', 'Zambia']
    visa_free = ['Barbados', 'Bhutan', 'Dominica', 'Grenada', 'Haiti', 'Hong Kong', 'Maldives', 'Mauritius', 'Montserrat', 'Nepal', 'Niue Island', 'Saint Vincent & the Grenadines', 'Samoa', 'Senegal', 'Serbia', 'Trinidad & Tobago']
    Visa_on_arrival = [
        'Angola', 'Bolivia', 'Cabo Verde', 'Cameroon', 'Cook Islands', 'Fiji', 'Guinea Bissau',
        'Indonesia', 'Iran', 'Jamaica', 'Jordan', 'Kiribati', 'Laos', 'Madagascar', 'Mauritania',
        'Nigeria', 'Qatar', 'Republic of Marshall Islands', 'Reunion Island', 'Rwanda', 'Seychelles',
        'Somalia', 'Tunisia', 'Tuvalu', 'Vanuatu', 'Zimbabwe'
    ]
    VoA_Evisa = [
        'Kenya', 'Myanmar', 'Saint Lucia', 'Sri Lanka', 'Suriname', 'Tajikistan', 'Tanzania',
        'Thailand', 'Vietnam', 'Ethiopia', 'Cambodia'
    ]
    
    if dest in e_visa:
        visa = "e-Visa Required"
    elif dest in visa_free:
        visa = "Visa-Free Access"
    elif dest in Visa_on_arrival:
        visa = "Visa on Arrival"
    elif dest in VoA_Evisa:
        visa = "Visa on Arrival or e-Visa available"
    else:
        visa = "Standard Visa Required"
        
    return {"visa_status": visa}

workflow = StateGraph(dict)
workflow.add_node("check_visa", visa_check_node)
workflow.add_edge(START, "check_visa")
workflow.add_edge("check_visa", END)
agent = workflow.compile()

@app.post("/api/chat")
async def chat(data: dict):
    user_message = data.get("message", "Thailand")
    response = agent.invoke({"destination": user_message})
    
    return {
        "reply": f"Thinking about {user_message}? Great choice! I've run the agentic checks for your Indian passport.",
        "visa": response["visa_status"],
        "agent_logs": "VisaCheckNode: Complete ✅"
    }"""
"""from fastapi import FastAPI, HTTPException, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from typing import Dict, Optional

app = FastAPI()

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Database
users_db: Dict[str, dict] = {}

class UserSignup(BaseModel):
    name: str
    email: str
    password: str

# --- AUTH ROUTES ---
@app.post("/api/signup")
async def signup(user: UserSignup):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.email] = {"name": user.name, "password": user.password}
    return {"message": "User created"}

@app.post("/api/login")
async def login(data: dict = Body(...)):
    user = users_db.get(data.get("identifier"))
    if not user or user["password"] != data.get("password"):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "ok"}

@app.post("/api/verify")
async def verify(response: Response):
    # Sets the cookie that the Next.js Middleware looks for
    response.set_cookie(key="aura_token", value="active_session", httponly=False)
    return {"status": "success"}

# --- AGENT LOGIC ---
def visa_check_node(state: dict):
    dest = state.get("destination", "").lower().capitalize()
    # ... (Your visa lists here) ...
    # Simplified for the code block:
    visa_free = ['Maldives', 'Mauritius', 'Bhutan', 'Nepal']
    status = "Visa-Free" if dest in visa_free else "Visa Required / E-Visa"
    return {"visa_status": status}

workflow = StateGraph(dict)
workflow.add_node("check_visa", visa_check_node)
workflow.add_edge(START, "check_visa")
workflow.add_edge("check_visa", END)
agent = workflow.compile()

@app.post("/api/chat")
async def chat(data: dict):
    response = agent.invoke({"destination": data.get("message")})
    return {"reply": f"Checking {data.get('message')}...", "visa": response["visa_status"]}"""

"""from fastapi import FastAPI, HTTPException, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from typing import Dict, Optional

app = FastAPI()

# Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Database
users_db: Dict[str, dict] = {}

class UserSignup(BaseModel):
    name: str
    email: str
    password: str

# --- AUTH ROUTES ---
@app.post("/api/signup")
async def signup(user: UserSignup):
    # Store user (In production, hash the password!)
    users_db[user.email] = {"name": user.name, "password": user.password}
    return {"message": "User created, OTP sent."}

@app.post("/api/login")
async def login(data: dict = Body(...)):
    user = users_db.get(data.get("identifier"))
    if not user or user["password"] != data.get("password"):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "ok"}

@app.post("/api/verify")
async def verify(response: Response):
    # Sets the cookie that tells the app the session is active
    response.set_cookie(key="aura_token", value="active_session", httponly=False)
    return {"status": "success"}

# --- AGENT LOGIC (Your Original Logic) ---
def visa_check_node(state: dict):
    dest = state.get("destination", "").lower().capitalize()
    # Your lists (simplified for the snippet)
    visa_free = ['Maldives', 'Mauritius', 'Bhutan', 'Nepal', 'Barbados']
    e_visa = ['Singapore', 'Thailand', 'Vietnam', 'Turkey']
    
    if dest in visa_free: status = "Visa-Free Access"
    elif dest in e_visa: status = "e-Visa / Visa on Arrival"
    else: status = "Standard Visa Required"
    
    return {"visa_status": status}

workflow = StateGraph(dict)
workflow.add_node("check_visa", visa_check_node)
workflow.add_edge(START, "check_visa")
workflow.add_edge("check_visa", END)
agent = workflow.compile()

@app.post("/api/chat")
async def chat(data: dict):
    response = agent.invoke({"destination": data.get("message")})
    return {"reply": f"Checks complete for {data.get('message')}.", "visa": response["visa_status"]}"""

from fastapi import FastAPI, HTTPException, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# 🛡️ SECURITY: Enable CORS for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Database (In-memory)
users_db: Dict[str, dict] = {}

class UserSignup(BaseModel):
    name: str
    email: str
    password: str

# --- AUTHENTICATION ROUTES ---
@app.post("/api/signup")
async def signup(user: UserSignup):
    users_db[user.email] = {"name": user.name, "password": user.password}
    print(f"✅ User Created: {user.email}")
    return {"message": "Signup successful"}

@app.post("/api/login")
async def login(data: dict = Body(...)):
    user = users_db.get(data.get("identifier"))
    if not user or user["password"] != data.get("password"):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"status": "ok"}

@app.post("/api/verify")
async def verify(response: Response):
    # 🍪 THE KEY: This cookie tells the browser the session is active
    response.set_cookie(
        key="aura_token", 
        value="active_session", 
        httponly=False, # Allows client-side check
        samesite="lax"
    )
    return {"status": "verified"}

# --- AGENTIC CHAT ROUTE ---
@app.post("/api/chat")
async def chat(data: dict):
    dest = data.get("message", "").capitalize()
    # Simplified Visa Agent Logic
    visa_free = ["Thailand", "Maldives", "Mauritius", "Bhutan", "Nepal", "Indonesia"]
    status = "Visa-Free Access" if dest in visa_free else "e-Visa / Visa Required"
    
    return {
        "reply": f"Processing your journey to {dest}...",
        "visa": status
    }