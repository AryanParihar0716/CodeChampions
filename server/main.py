import os
import json
from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from sqlalchemy.orm import Session

# LangGraph & Agent Imports
from langgraph.graph import StateGraph, START, END
from agents import AGENT_REGISTRY, CHAT_AGENT
from agents.router import router_node, select_agents_for_query
from agents.state import TravelState

# Database imports
from database import get_db, User, SearchHistory

from pathlib import Path

_root = Path(__file__).resolve().parent.parent
_env_file = _root / ".env"
if not _env_file.exists():
    _env_file = _root / ".env.example"  # fallback for dev
load_dotenv(_env_file)

# --- Groq Client ---
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(title="AURA Agentic Core")

# --- 1. SECURITY SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. DATA MODELS ---
class UserSignup(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    identifier: str
    password: str

class VerifyRequest(BaseModel):
    email: str
    otp: str

class UserPreferencesUpdate(BaseModel):
    origin_city: str = None
    preferred_currency: str = None
    budget_range_min: float = None
    budget_range_max: float = None
    travel_style: str = None
    group_size: int = None
    preferred_airlines: list = None
    preferred_hotel_types: list = None
    dietary_restrictions: list = None
    accessibility_needs: list = None

# --- 3. AUTH ROUTES ---

@app.post("/api/signup")
async def signup(user: UserSignup, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user with default preferences
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,  # In production, hash this!
        verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"✅ User Registered: {user.email}")
    return {"message": "Signup successful"}

@app.post("/api/verify")
async def verify(request: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or str(request.otp) != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user.verified = True
    db.commit()
    return {"message": "Success"}

@app.post("/api/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.email == user.identifier) | (User.name == user.identifier)
    ).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "OK",
        "name": db_user.name,
        "user_id": db_user.id,
        "preferences": {
            "origin_city": db_user.origin_city,
            "preferred_currency": db_user.preferred_currency,
            "budget_range_min": db_user.budget_range_min,
            "budget_range_max": db_user.budget_range_max,
            "travel_style": db_user.travel_style,
            "group_size": db_user.group_size,
            "preferred_airlines": db_user.preferred_airlines,
            "preferred_hotel_types": db_user.preferred_hotel_types,
            "dietary_restrictions": db_user.dietary_restrictions,
            "accessibility_needs": db_user.accessibility_needs,
        }
    }

@app.put("/api/user/preferences")
async def update_preferences(
    preferences: UserPreferencesUpdate,
    user_id: int = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only provided fields
    update_data = preferences.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    return {"message": "Preferences updated successfully"}

# --- 4. AGENTIC ENGINE ---

def build_aura_graph():
    graph = StateGraph(TravelState)
    graph.add_node("router", router_node)
    graph.add_edge(START, "router")

    # Add all travel data agents
    for name, info in AGENT_REGISTRY.items():
        graph.add_node(name, info["node_fn"])
        graph.add_edge(name, END)

    # Add the chat agent
    for name, info in CHAT_AGENT.items():
        graph.add_node(name, info["node_fn"])
        graph.add_edge(name, END)

    def route_logic(state: dict):
        """Route based on intent and query content."""
        intent = state.get("intent", "travel_search")
        if intent == "chat":
            return ["chat"]

        # For travel searches, dynamically select agents based on query and user preferences
        message = state.get("message", "")
        user_prefs = state.get("user_preferences", {})
        selected_agents = select_agents_for_query(message, user_prefs)
        return selected_agents

    # Build the routing map (all possible targets)
    all_targets = {n: n for n in AGENT_REGISTRY.keys()}
    all_targets["chat"] = "chat"
    graph.add_conditional_edges("router", route_logic, all_targets)
    return graph.compile()

aura_engine = build_aura_graph()


# --- 5. GROQ AI RESPONSE SYNTHESIS ---

def synthesize_reply(user_query: str, agent_data: dict) -> str:
    """
    Use Groq (Llama 3.3) to generate a natural, conversational reply
    based on the structured data returned by the travel agents.
    """
    # Build a context summary from all agent results
    context_parts = [f"User asked: \"{user_query}\""]
    context_parts.append(f"Destination: {agent_data.get('destination', 'Unknown')}")

    if agent_data.get("flight_result"):
        flights = agent_data["flight_result"].get("flights", [])
        if flights:
            flight_info = ", ".join(
                f"{f.get('airline', '?')} at {f.get('price', 'N/A')}" for f in flights
            )
            context_parts.append(f"Flights found: {flight_info}")

    if agent_data.get("hotel_result"):
        hotels = agent_data["hotel_result"].get("hotels", [])
        if hotels:
            hotel_info = ", ".join(
                f"{h.get('name', '?')} at {h.get('price', 'N/A')}/night" for h in hotels
            )
            context_parts.append(f"Hotels found: {hotel_info}")

    if agent_data.get("weather_result"):
        wr = agent_data["weather_result"]
        context_parts.append(
            f"Weather: {wr.get('temp', '?')}, {wr.get('condition', '?')}, humidity {wr.get('humidity', '?')}"
        )

    if agent_data.get("visa_result"):
        vr = agent_data["visa_result"]
        context_parts.append(f"Visa: {vr.get('status', '?')} — {vr.get('detail', '')}")

    if agent_data.get("reviews_result"):
        rr = agent_data["reviews_result"]
        avg_rating = rr.get("average_rating", 0)
        if avg_rating > 0:
            context_parts.append(f"Reviews: Average {avg_rating}/5 stars from {rr.get('total_reviews', 0)} reviews")

    if agent_data.get("social_trends_result"):
        sr = agent_data["social_trends_result"]
        trends = sr.get("trends", [])
        if trends:
            top_trend = trends[0].get("hashtag", "")
            context_parts.append(f"Social Trends: {top_trend} is trending with {len(trends)} related hashtags")

    if agent_data.get("price_history_result"):
        pr = agent_data["price_history_result"]
        flight_trend = pr.get("flight_trend", {})
        hotel_trend = pr.get("hotel_trend", {})
        if flight_trend.get("direction") != "stable":
            context_parts.append(f"Price Trends: Flight prices are {flight_trend.get('direction')} by {flight_trend.get('change_percent', 0)}%")

    if agent_data.get("events_result"):
        er = agent_data["events_result"]
        events = er.get("events", [])
        if events:
            context_parts.append(f"Events: {len(events)} upcoming events found, including {events[0].get('name', '')[:30]}...")

    if agent_data.get("currency_result"):
        cr = agent_data["currency_result"]
        dest_currency = cr.get("destination_currency", {})
        if dest_currency:
            context_parts.append(f"Currency: Local currency is {dest_currency.get('name', '')} ({dest_currency.get('code', '')})")

    if agent_data.get("advisories_result"):
        ar = agent_data["advisories_result"]
        risk_level = ar.get("overall_risk", "unknown")
        if risk_level != "normal":
            context_parts.append(f"Safety: {risk_level.replace('_', ' ').title()} advisory in effect")

    if agent_data.get("transport_result"):
        tr = agent_data["transport_result"]
        options = tr.get("options", [])
        if options:
            context_parts.append(f"Transport: {len(options)} transportation options available including {options[0].get('type', '')}")

    if agent_data.get("attractions_result"):
        atr = agent_data["attractions_result"]
        attractions = atr.get("attractions", [])
        restaurants = atr.get("restaurants", [])
        if attractions or restaurants:
            context_parts.append(f"Attractions: {len(attractions)} attractions and {len(restaurants)} restaurants recommended")

    if agent_data.get("recommendation_result"):
        rr = agent_data["recommendation_result"]
        recommendations = rr.get("recommendations", [])
        itinerary = rr.get("itinerary")
        if recommendations:
            context_parts.append(f"Personalized Recommendations: {len(recommendations)} tailored suggestions based on your preferences")
        if itinerary:
            context_parts.append(f"Itinerary: Complete {itinerary.get('duration', '3-5 day')} travel plan generated")

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are AURA, a premium AI travel assistant. Write short, conversational, helpful replies (2-4 sentences max). Be warm and knowledgeable. Mention specific details like prices, weather, or visa status if available. Do NOT use markdown or bullet points — just plain flowing text.",
                },
                {"role": "user", "content": context},
            ],
            temperature=0.7,
            max_tokens=256,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ Groq synthesis failed: {e}")
        return f"AURA has compiled travel intelligence for {agent_data.get('destination', 'your destination')}."


# --- 6. CHAT ENDPOINT ---

@app.post("/api/chat")
async def chat(data: dict = Body(...), db: Session = Depends(get_db)):
    query = data.get("message", "")
    user_id = data.get("user_id")  # Optional user ID for personalization

    # Get user preferences if user_id provided
    user_preferences = None
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user_preferences = {
                "origin_city": user.origin_city,
                "preferred_currency": user.preferred_currency,
                "budget_range_min": user.budget_range_min,
                "budget_range_max": user.budget_range_max,
                "travel_style": user.travel_style,
                "group_size": user.group_size,
                "preferred_airlines": user.preferred_airlines,
                "preferred_hotel_types": user.preferred_hotel_types,
                "dietary_restrictions": user.dietary_restrictions,
                "accessibility_needs": user.accessibility_needs,
            }

    # Run the agentic workflow with user preferences
    initial_state = {"message": query}
    if user_preferences:
        initial_state["user_preferences"] = user_preferences
    if user_id:
        initial_state["user_id"] = user_id

    final_state = aura_engine.invoke(initial_state)

    intent = final_state.get("intent", "travel_search")

    # Store search history if user_id provided
    if user_id:
        search_history = SearchHistory(
            user_id=user_id,
            query=query,
            destination=final_state.get("destination"),
            intent=intent,
            results_summary={
                "has_flights": bool(final_state.get("flight_result")),
                "has_hotels": bool(final_state.get("hotel_result")),
                "has_weather": bool(final_state.get("weather_result")),
                "has_visa": bool(final_state.get("visa_result")),
            }
        )
        db.add(search_history)
        db.commit()

    # If it was a chat-only intent, return the chat agent's reply directly
    if intent == "chat":
        chat_result = final_state.get("chat_result", {})
        return {
            "reply": chat_result.get("reply", "How can I help with your travel plans?"),
            "destination": None,
            "flight_result": None,
            "hotel_result": None,
            "weather_result": None,
            "visa_result": None,
        }

    # Otherwise, collect structured results from travel agents
    agent_data = {
        "destination": final_state.get("destination"),
        "flight_result": final_state.get("flight_result"),
        "hotel_result": final_state.get("hotel_result"),
        "weather_result": final_state.get("weather_result"),
        "visa_result": final_state.get("visa_result"),
        "reviews_result": final_state.get("reviews_result"),
        "social_trends_result": final_state.get("social_trends_result"),
        "price_history_result": final_state.get("price_history_result"),
        "events_result": final_state.get("events_result"),
        "currency_result": final_state.get("currency_result"),
        "advisories_result": final_state.get("advisories_result"),
        "transport_result": final_state.get("transport_result"),
        "attractions_result": final_state.get("attractions_result"),
        "recommendation_result": final_state.get("recommendation_result"),
    }

    # Generate AI reply using Groq
    ai_reply = synthesize_reply(query, agent_data)

    return {
        "reply": ai_reply,
        **agent_data,
    }

# --- 7. HEALTH CHECK ---
@app.get("/api/health")
async def health():
    return {"status": "online", "agents": list(AGENT_REGISTRY.keys())}