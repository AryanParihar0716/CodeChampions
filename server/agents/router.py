"""
Intent Router — decides which agent(s) to activate.

Uses keyword matching for zero-cost, instant routing.
To upgrade to LLM-based routing, replace `detect_intent()` with an LLM call.
"""

# Map of intent name -> trigger keywords
INTENT_KEYWORDS: dict[str, list[str]] = {
    "visa":    ["visa", "passport", "entry", "permit", "immigration", "document"],
    "flight":  ["flight", "fly", "plane", "airline", "airfare", "ticket", "departure"],
    "hotel":   ["hotel", "stay", "book", "room", "resort", "accommodation", "hostel"],
    "weather": ["weather", "climate", "temperature", "rain", "forecast", "season"],
}


def detect_intent(message: str) -> str:
    """
    Scan the user message for keywords and return the matching intent.
    If no specific intent is found, return "all" to run every agent.
    """
    msg_lower = message.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in msg_lower for kw in keywords):
            return intent
    return "all"  # No specific intent → run everything


def router_node(state: dict) -> dict:
    """LangGraph node: extracts destination and detects intent."""
    message = state.get("message", "")

    # Simple destination extraction: strip out known keywords, use what's left
    destination = message
    for keywords in INTENT_KEYWORDS.values():
        for kw in keywords:
            destination = destination.lower().replace(kw, "")
    destination = destination.strip().title() or message.strip().title()

    return {
        "destination": destination,
        "intent": detect_intent(message),
    }
