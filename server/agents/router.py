"""
Intent Router — decides which agent(s) to activate.

Detects whether the user wants:
  - "travel_search" → triggers flight, hotel, weather, visa agents
  - "chat" → triggers the conversational chat agent only
"""

import dateparser
from datetime import datetime, timedelta
from .utils import IATA_MAP
from typing import List

# Keywords that indicate the user wants live travel data
TRAVEL_KEYWORDS = [
    "flight", "fly", "plane", "airline", "airfare", "ticket", "departure", "booking",
    "hotel", "stay", "book", "room", "resort", "accommodation", "hostel",
    "visa", "passport", "entry", "permit", "immigration", "document",
    "weather", "climate", "temperature", "rain", "forecast", "season",
    "trip", "travel", "vacation", "package",
]

# Keywords that indicate casual chat / suggestions
CHAT_KEYWORDS = [
    "hello", "hi", "hey", "help", "suggest", "recommend", "best", "should",
    "where", "when", "what", "which", "compare", "tips", "advice", "plan",
    "budget", "cheap", "luxury", "honeymoon", "solo", "family", "adventure",
    "safe", "food", "culture", "thank", "thanks", "bye", "how are",
]


def detect_intent(message: str) -> str:
    """
    Classify the user message as 'travel_search' or 'chat'.

    If the message contains a known city + travel keywords → travel_search
    If it's a greeting, suggestion request, or general question → chat
    """
    msg_lower = message.lower()

    # Check if any known city is mentioned
    has_city = any(city.lower() in msg_lower for city in IATA_MAP.keys())

    # Check for travel action keywords
    has_travel_kw = any(kw in msg_lower for kw in TRAVEL_KEYWORDS)

    # If a city is mentioned AND a travel keyword → they want real data
    if has_city and has_travel_kw:
        return "travel_search"

    # If a city is mentioned with no other context, still search
    if has_city and len(message.split()) <= 4:
        return "travel_search"

    # If they have strong travel keywords but no city, still do travel search
    # (the router will default to empty and the agents handle it gracefully)
    strong_travel = ["flight", "hotel", "visa", "weather", "book", "ticket"]
    if any(kw in msg_lower for kw in strong_travel):
        return "travel_search"

    # Otherwise it's conversational chat
    return "chat"


def router_node(state: dict) -> dict:
    """LangGraph node: extracts destination, dates, and detects intent."""
    msg = state.get("message", "")
    user_prefs = state.get("user_preferences", {})
    words = msg.strip().split()

    # 1. Detect intent
    intent = detect_intent(msg)

    # For chat-only messages, skip destination/date extraction
    if intent == "chat":
        print(f"💬 Router: Chat intent detected for '{msg[:40]}...'")
        return {
            "destination": "",
            "start_date": None,
            "end_date": None,
            "intent": "chat",
        }

    # 2. Date extraction (only for travel searches)
    settings = {"PREFER_DATES_FROM": "future"}
    start_dt = dateparser.parse(msg, settings=settings)
    start_date = (
        start_dt.strftime("%Y-%m-%d")
        if start_dt
        else (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    )
    end_date = (
        datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=5)
    ).strftime("%Y-%m-%d")

    # 3. Destination extraction
    city = ""  # No default — agents handle missing destination gracefully
    msg_lower = msg.lower()

    # Priority 1: Direct match from IATA registry
    norm_map = {k.lower().replace(" ", ""): k for k in IATA_MAP.keys()}
    for word in words:
        clean_word = word.lower().strip("?!.,")
        if clean_word in norm_map:
            city = norm_map[clean_word]
            break

    # Priority 2: Geography triggers (in, to, at)
    if not city:
        triggers = ["in", "to", "at", "for"]
        words_lower = [w.lower() for w in words]
        for i, word in enumerate(words_lower):
            if word in triggers and i + 1 < len(words):
                potential = words[i + 1].strip("?!.,").title()
                if potential not in ["Next", "The", "A", "This", "My"]:
                    city = potential
                    break

    # 4. Apply user preferences for origin and other defaults
    origin_city = user_prefs.get("origin_city", "Mumbai") if user_prefs else "Mumbai"
    group_size = user_prefs.get("group_size", 2) if user_prefs else 2

    print(f"🧠 Router: travel_search → {city} from {origin_city} on {start_date} (group: {group_size})")
    return {
        "destination": city,
        "start_date": start_date,
        "end_date": end_date,
        "origin_city": origin_city,
        "group_size": group_size,
        "user_preferences": user_prefs,  # Pass through for agents
        "intent": "travel_search",
    }


def select_agents_for_query(message: str, user_prefs: dict = None) -> List[str]:
    """Select which agents to run based on query content and user preferences."""
    from typing import List
    msg_lower = message.lower()

    # Base agents always run for travel searches
    selected_agents = ["flight", "hotel", "weather", "visa"]

    # Additional agents based on query keywords
    agent_keywords = {
        "reviews": ["review", "rating", "rated", "recommended"],
        "social_trends": ["trendy", "popular", "hot", "buzzing", "instagram", "twitter"],
        "price_history": ["price", "cost", "expensive", "cheap", "deal", "trend"],
        "events": ["event", "festival", "concert", "show", "celebration", "activity"],
        "currency": ["exchange", "rate", "convert", "money", "budget"],
        "advisories": ["safe", "danger", "warning", "advisory", "risk"],
        "transport": ["transport", "bus", "train", "taxi", "metro", "travel"],
        "attractions": ["see", "visit", "attraction", "sightseeing", "restaurant", "food", "eat"],
        "recommendation": ["recommend", "suggest", "itinerary", "plan", "personalized", "best for me", "tailored"]
    }

    for agent, keywords in agent_keywords.items():
        if any(keyword in msg_lower for keyword in keywords):
            selected_agents.append(agent)

    # Additional agents based on user preferences
    if user_prefs:
        # If user has dietary restrictions, include attractions for restaurant filtering
        if user_prefs.get("dietary_restrictions") and len(user_prefs["dietary_restrictions"]) > 0:
            if "attractions" not in selected_agents:
                selected_agents.append("attractions")
                print("🍽️ Including attractions agent for dietary preferences")

        # If user has accessibility needs, include transport and attractions
        if user_prefs.get("accessibility_needs") and len(user_prefs["accessibility_needs"]) > 0:
            if "transport" not in selected_agents:
                selected_agents.append("transport")
            if "attractions" not in selected_agents:
                selected_agents.append("attractions")
            print("♿ Including transport/attractions agents for accessibility needs")

        # If user has budget constraints, include price history
        if user_prefs.get("budget_range_min") or user_prefs.get("budget_range_max"):
            if "price_history" not in selected_agents:
                selected_agents.append("price_history")
            print("💰 Including price history agent for budget analysis")

        # If user prefers certain airlines, ensure reviews agent runs for airline feedback
        if user_prefs.get("preferred_airlines") and len(user_prefs["preferred_airlines"]) > 0:
            if "reviews" not in selected_agents:
                selected_agents.append("reviews")
            print("✈️ Including reviews agent for preferred airlines")

    # Remove duplicates
    selected_agents = list(set(selected_agents))

    print(f"🎯 Selected agents: {selected_agents}")
    return selected_agents