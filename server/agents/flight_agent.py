"""
Flight Search Agent — returns mock flight options.

To upgrade: replace `_mock_flights()` with an Amadeus Flight Offers API call.
Docs: https://developers.amadeus.com/self-service/category/flights
"""

import random

# Mock flight data pool
_AIRLINES = {
    "Air India": {"code": "AI", "class": "Full Service"},
    "IndiGo": {"code": "6E", "class": "Low Cost"},
    "Vistara": {"code": "UK", "class": "Full Service"},
    "SpiceJet": {"code": "SG", "class": "Low Cost"},
    "Emirates": {"code": "EK", "class": "Premium"},
    "Singapore Airlines": {"code": "SQ", "class": "Premium"},
    "Thai Airways": {"code": "TG", "class": "Full Service"},
    "Qatar Airways": {"code": "QR", "class": "Premium"},
}

_MOCK_FLIGHTS_BY_REGION: dict[str, list[dict]] = {
    "default": [
        {"airline": "Air India", "price": "₹28,500", "duration": "6h 30m", "departure": "06:15", "stops": "Non-stop"},
        {"airline": "Emirates", "price": "₹42,000", "duration": "8h 15m", "departure": "14:30", "stops": "1 stop (DXB)"},
        {"airline": "IndiGo", "price": "₹22,300", "duration": "7h 45m", "departure": "23:55", "stops": "1 stop (DEL)"},
    ],
    "southeast_asia": [
        {"airline": "IndiGo", "price": "₹12,800", "duration": "4h 30m", "departure": "05:45", "stops": "Non-stop"},
        {"airline": "Thai Airways", "price": "₹18,500", "duration": "4h 15m", "departure": "10:30", "stops": "Non-stop"},
        {"airline": "SpiceJet", "price": "₹9,999", "duration": "5h 50m", "departure": "22:10", "stops": "1 stop (CCU)"},
    ],
    "middle_east": [
        {"airline": "Emirates", "price": "₹15,200", "duration": "3h 45m", "departure": "02:15", "stops": "Non-stop"},
        {"airline": "Air India", "price": "₹12,400", "duration": "4h 00m", "departure": "09:00", "stops": "Non-stop"},
        {"airline": "Qatar Airways", "price": "₹18,900", "duration": "5h 20m", "departure": "16:45", "stops": "1 stop (DOH)"},
    ],
}

_REGION_MAP: dict[str, str] = {
    "Thailand": "southeast_asia", "Vietnam": "southeast_asia", "Singapore": "southeast_asia",
    "Malaysia": "southeast_asia", "Cambodia": "southeast_asia", "Indonesia": "southeast_asia",
    "Uae": "middle_east", "United Arab Emirates": "middle_east", "Dubai": "middle_east",
    "Oman": "middle_east", "Bahrain": "middle_east", "Qatar": "middle_east",
}


def _get_flights(destination: str) -> list[dict]:
    region = _REGION_MAP.get(destination, "default")
    return _MOCK_FLIGHTS_BY_REGION[region]


def flight_node(state: dict) -> dict:
    """LangGraph node: searches for flights to the destination."""
    dest = state.get("destination", "").strip().title()
    flights = _get_flights(dest)

    return {
        "flight_result": {
            "destination": dest,
            "flights": flights,
            "result_count": len(flights),
            "agent": "Flight Search Agent",
        }
    }
