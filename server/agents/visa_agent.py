"""
Visa Compliance Agent — checks visa requirements for Indian passport holders.

To upgrade: replace the hardcoded lists with a Sherpa° API call.
"""

VISA_FREE = [
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
    """LangGraph node: checks visa status for the destination."""
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
