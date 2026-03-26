from fastapi import FastAPI, HTTPException, Response, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from graph import compiled_graph

app = FastAPI(title="AURA Travel Agent", version="2.0")

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
    response.set_cookie(key="aura_token", value="active_session", httponly=False)
    return {"status": "success"}


# --- AGENTIC CHAT ROUTE ---
@app.post("/api/chat")
async def chat(data: dict = Body(...)):
    """
    Send user message through the multi-agent graph.
    Returns results from all activated agents.
    """
    message = data.get("message", "")

    # Run the LangGraph
    result = compiled_graph.invoke({"message": message})

    # Build response with all agent results
    response = {
        "reply": f"AURA agents completed analysis for '{result.get('destination', message)}'.",
        "intent": result.get("intent", "all"),
        "destination": result.get("destination", message),
    }

    # Attach each agent's result if present
    if result.get("visa_result"):
        response["visa"] = result["visa_result"]
    if result.get("flight_result"):
        response["flights"] = result["flight_result"]
    if result.get("hotel_result"):
        response["hotels"] = result["hotel_result"]
    if result.get("weather_result"):
        response["weather"] = result["weather_result"]

    return response