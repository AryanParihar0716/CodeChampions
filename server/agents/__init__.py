"""
Agent Registry — maps agent names to their node functions.

To add a new agent:
  1. Create a file named `<name>_agent.py` in this folder
  2. Define a function named `<name>_node(state: dict) -> dict`
  3. Register it below
"""

from .flight_agent import flight_node
from .hotel_agent import hotel_node
from .weather_agent import weather_node
from .visa_agent import visa_node
from .chat_agent import chat_node
from .reviews_agent import reviews_node
from .social_agent import social_trends_node
from .price_history_agent import price_history_node
from .events_agent import events_node
from .currency_agent import currency_node
from .advisories_agent import advisories_node
from .transport_agent import transport_node
from .attractions_agent import attractions_node
from .recommendation_agent import recommendation_node

# Travel data agents — triggered on travel_search intent
AGENT_REGISTRY = {
    "flight": {
        "node_fn": flight_node,
        "description": "Searches for real-time flight data via Skyscanner",
    },
    "hotel": {
        "node_fn": hotel_node,
        "description": "Finds premium hotel accommodations",
    },
    "weather": {
        "node_fn": weather_node,
        "description": "Provides weather forecasts for the destination",
    },
    "visa": {
        "node_fn": visa_node,
        "description": "Visa Intelligence Agent",
    },
    "reviews": {
        "node_fn": reviews_node,
        "description": "Fetches user reviews and ratings for attractions",
    },
    "social_trends": {
        "node_fn": social_trends_node,
        "description": "Analyzes social media trends for destinations",
    },
    "price_history": {
        "node_fn": price_history_node,
        "description": "Tracks historical pricing trends",
    },
    "events": {
        "node_fn": events_node,
        "description": "Finds local events and seasonal activities",
    },
    "currency": {
        "node_fn": currency_node,
        "description": "Provides currency exchange rates",
    },
    "advisories": {
        "node_fn": advisories_node,
        "description": "Fetches travel advisories and safety warnings",
    },
    "transport": {
        "node_fn": transport_node,
        "description": "Provides local transportation options",
    },
    "attractions": {
        "node_fn": attractions_node,
        "description": "Recommends attractions and dining options",
    },
    "recommendation": {
        "node_fn": recommendation_node,
        "description": "Generates personalized travel recommendations and itineraries",
    },
}

# Chat agent — triggered on chat intent (conversational Gemini)
CHAT_AGENT = {
    "chat": {
        "node_fn": chat_node,
        "description": "AI-powered travel concierge for suggestions and chat",
    },
}