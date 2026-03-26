"""
Hotel Search Agent — returns mock hotel options.

To upgrade: replace `_get_hotels()` with an Amadeus Hotel Search API call
or Duffel Stays API.
"""

_MOCK_HOTELS_BY_REGION: dict[str, list[dict]] = {
    "default": [
        {
            "name": "Grand Hyatt",
            "stars": 5,
            "price_per_night": "₹12,500",
            "amenities": ["Pool", "Spa", "Gym", "Free Wi-Fi", "Airport Shuttle"],
            "rating": 4.6,
        },
        {
            "name": "Novotel City Centre",
            "stars": 4,
            "price_per_night": "₹6,800",
            "amenities": ["Free Wi-Fi", "Restaurant", "Gym", "Business Centre"],
            "rating": 4.2,
        },
        {
            "name": "OYO Townhouse",
            "stars": 3,
            "price_per_night": "₹2,200",
            "amenities": ["Free Wi-Fi", "AC", "TV", "Breakfast"],
            "rating": 3.8,
        },
    ],
    "luxury": [
        {
            "name": "The Ritz-Carlton",
            "stars": 5,
            "price_per_night": "₹35,000",
            "amenities": ["Private Beach", "Spa", "Fine Dining", "Butler Service"],
            "rating": 4.9,
        },
        {
            "name": "Four Seasons Resort",
            "stars": 5,
            "price_per_night": "₹28,000",
            "amenities": ["Infinity Pool", "Spa", "Water Sports", "Kids Club"],
            "rating": 4.8,
        },
        {
            "name": "Taj Exotica",
            "stars": 5,
            "price_per_night": "₹22,000",
            "amenities": ["Beach Villa", "Ayurvedic Spa", "Yoga", "Snorkeling"],
            "rating": 4.7,
        },
    ],
    "budget": [
        {
            "name": "Backpacker's Hub",
            "stars": 2,
            "price_per_night": "₹800",
            "amenities": ["Free Wi-Fi", "Shared Kitchen", "Laundry"],
            "rating": 4.1,
        },
        {
            "name": "City Hostel",
            "stars": 2,
            "price_per_night": "₹1,200",
            "amenities": ["Free Wi-Fi", "AC", "Locker", "Common Area"],
            "rating": 3.9,
        },
        {
            "name": "FabHotel Prime",
            "stars": 3,
            "price_per_night": "₹1,800",
            "amenities": ["Free Wi-Fi", "AC", "TV", "Breakfast"],
            "rating": 3.7,
        },
    ],
}

_DESTINATION_TIER: dict[str, str] = {
    "Maldives": "luxury", "Mauritius": "luxury", "Dubai": "luxury",
    "Uae": "luxury", "United Arab Emirates": "luxury",
    "Switzerland": "luxury", "France": "luxury",
    "Thailand": "budget", "Vietnam": "budget", "Cambodia": "budget",
    "Nepal": "budget", "Indonesia": "budget", "Laos": "budget",
}


def _get_hotels(destination: str) -> list[dict]:
    tier = _DESTINATION_TIER.get(destination, "default")
    return _MOCK_HOTELS_BY_REGION[tier]


def hotel_node(state: dict) -> dict:
    """LangGraph node: searches for hotels at the destination."""
    dest = state.get("destination", "").strip().title()
    hotels = _get_hotels(dest)

    return {
        "hotel_result": {
            "destination": dest,
            "hotels": hotels,
            "result_count": len(hotels),
            "agent": "Hotel Search Agent",
        }
    }
