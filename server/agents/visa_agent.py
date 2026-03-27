"""
Visa Compliance Agent — checks visa requirements for Indian passport holders.

To upgrade: replace the hardcoded lists with a Sherpa° API call.
"""

"""VISA_FREE = [
    "Maldives", "Mauritius", "Bhutan", "Nepal", "Barbados",
    "Serbia", "Indonesia", "Fiji", "Jamaica", "Haiti",
    "Dominica", "Grenada", "Trinidad And Tobago", "Vanuatu",
]

E_VISA = [
    "Singapore", "Thailand", "Vietnam", "Turkey", "Malaysia",
    "Sri Lanka", "Myanmar", "Cambodia", "Laos", "Australia",
    "Kenya", "Ethiopia", "Tanzania", "Oman", "Bahrain",
    "South Korea", "Japan", "Uae", "United Arab Emirates",
]

STRICT_VISA = [
    "United States", "Usa", "United Kingdom", "Uk", "Canada",
    "Germany", "France", "Italy", "Spain", "Netherlands",
    "Switzerland", "Sweden", "Norway", "Denmark", "Belgium",
    "Austria", "Ireland", "Portugal", "New Zealand", "China", "Russia",
]


def visa_node(state: dict) -> dict:
    LangGraph node: checks visa status for the destination.
    dest = state.get("destination", "").strip().title()

    if dest in VISA_FREE:
        status = "✅ Visa-Free Access"
        detail = "No visa required for Indian passport holders. You can travel freely!"
    elif dest in E_VISA:
        status = "⚡ e-Visa / Visa on Arrival"
        detail = "Apply for an e-Visa online before departure, or get a Visa on Arrival."
    elif dest in STRICT_VISA:
        status = "📋 Standard Visa Required"
        detail = "You must apply at the embassy/consulate. Processing takes 2-4 weeks."
    else:
        status = "❓ Visa Status Unknown"
        detail = f"Could not find visa data for '{dest}'. Please check with the embassy."

    return {
        "visa_result": {
            "destination": dest,
            "status": status,
            "detail": detail,
            "agent": "Visa Compliance Agent",
        }
    }
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def visa_node(state: dict) -> dict:
    # 1. Get destination from state
    dest = state.get("destination", "").strip().title()
    
    # 2. Build a high-precision query for Indian Citizens
    query = f"visa requirements for Indian passport holders to {dest} March 2026"
    print(f"🛂 VISA API: Searching live requirements for {dest}...")

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "gl": "in" # Geolocation: India (to get India-specific results)
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        
        # 3. Extract the "Knowledge"
        # We check the Answer Box first (Google's direct answer), then snippets
        answer = data.get("answer_box", {}).get("answer") or \
                 data.get("answer_box", {}).get("snippet") or \
                 data.get("organic_results", [{}])[0].get("snippet", "No immediate details found.")

        # 4. Simple Logic to assign a status based on search text
        status = "📋 Standard Visa"
        low_text = answer.lower()
        
        if "visa free" in low_text or "no visa" in low_text:
            status = "✅ Visa-Free Access"
        elif "evisa" in low_text or "e-visa" in low_text or "on arrival" in low_text:
            status = "⚡ e-Visa / Arrival"
        elif "restricted" in low_text or "banned" in low_text:
            status = "🚫 Entry Restricted"

        return {
            "visa_result": {
                "destination": dest,
                "status": status,
                "detail": answer[:180] + "...", # Clean up the text for the card
                "agent": "Visa Intelligence Agent"
            }
        }

    except Exception as e:
        print(f"❌ Visa Agent Error: {e}")
        return {
            "visa_result": {
                "destination": dest,
                "status": "❓ Verification Required",
                "detail": "Live data stream interrupted. Please check with the official embassy.",
                "agent": "Visa Intelligence Agent"
            }
        }