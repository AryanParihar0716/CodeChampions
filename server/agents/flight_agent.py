"""
Flight Search Agent — uses Flights Sky API via RapidAPI.
Searches for one-way flights from Mumbai (BOM) to the destination.

API: https://rapidapi.com/ntd119/api/flights-sky
"""

import os
import requests
from .utils import get_iata

RAPIDAPI_HOST = "flights-sky.p.rapidapi.com"


def flight_node(state: dict) -> dict:
    """LangGraph node: searches for flights via Flights Sky API."""
    city = state.get("destination", "")
    start_date = state.get("start_date")
    origin_city = state.get("origin_city", "Mumbai")  # Use user's preferred origin
    user_prefs = state.get("user_prefs", {})
    api_key = os.getenv("RAPIDAPI_KEY")

    if not api_key:
        print("❌ RAPIDAPI_KEY not set")
        return {"flight_result": {"flights": []}}

    # Cross-agent data integration
    weather_data = state.get("weather_result", {})
    hotel_data = state.get("hotel_result", {}).get("hotels", [])
    price_history = state.get("price_history_result", {})

    # Extract user preferences for filtering
    budget_max = user_prefs.get("budget_range", {}).get("max")
    preferred_airlines = user_prefs.get("preferred_airlines", [])

    print(f"✈️ Flight Agent: Searching flights from {origin_city} to {city}...")

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    # The API accepts IATA codes directly as fromEntityId/toEntityId
    params = {
        "fromEntityId": get_iata(origin_city),
        "toEntityId": get_iata(city),
        "departDate": start_date or "",
        "currency": "INR",
    }

    try:
        res = requests.get(
            f"https://{RAPIDAPI_HOST}/flights/search-one-way",
            headers=headers,
            params=params,
            timeout=15,
        )
        data = res.json()

        itineraries = data.get("data", {}).get("itineraries", [])
        flights = []

        for it in itineraries[:15]:  # Get more results for cross-agent filtering
            price = it.get("price", {}).get("formatted", "N/A")

            # Extract numeric price for filtering
            price_numeric = None
            if "₹" in price:
                try:
                    price_numeric = float(price.replace("₹", "").replace(",", ""))
                except:
                    pass

            legs = it.get("legs", [])
            if not legs:
                continue

            leg = legs[0]
            carriers = leg.get("carriers", {}).get("marketing", [])
            airline = carriers[0].get("name", "Unknown") if carriers else "Unknown"
            logo = carriers[0].get("logoUrl", "") if carriers else ""
            duration = leg.get("durationInMinutes", 0)
            stops = leg.get("stopCount", 0)

            flight_data = {
                "airline": airline,
                "price": price,
                "price_numeric": price_numeric,
                "logo": logo,
                "duration": f"{duration // 60}h {duration % 60}m",
                "stops": f"{stops} stop{'s' if stops != 1 else ''}" if stops else "Non-stop",
                "cross_agent_score": 0,
                "recommendation_reasons": []
            }

            # Apply user preference filters
            include_flight = True

            # Budget filtering
            if budget_max and price_numeric and price_numeric > budget_max:
                include_flight = False

            # Preferred airlines filtering
            if preferred_airlines:
                airline_lower = airline.lower()
                airline_match = any(pref.lower() in airline_lower for pref in preferred_airlines)
                if not airline_match:
                    include_flight = False

            # Cross-agent filtering and scoring
            if include_flight:
                cross_score, reasons = _calculate_flight_cross_score(
                    flight_data, weather_data, hotel_data, price_history
                )
                flight_data["cross_agent_score"] = cross_score
                flight_data["recommendation_reasons"].extend(reasons)

                flights.append(flight_data)

        # Sort by cross-agent score and limit to top 5
        flights.sort(key=lambda x: x["cross_agent_score"], reverse=True)
        flights = flights[:5]

        print(f"✅ Found {len(flights)} flights to {city} (after filtering)")
        return {"flight_result": {"flights": flights}}

    except Exception as e:
        print(f"❌ Flight search error: {e}")
        return {"flight_result": {"flights": []}}


def _calculate_flight_cross_score(flight_data: dict, weather_data: dict,
                                hotel_data: list, price_history: dict) -> tuple:
    """Calculate a cross-agent recommendation score for the flight."""
    score = 0
    reasons = []

    # Base score from price (lower price = higher score)
    price_numeric = flight_data.get("price_numeric")
    if price_numeric:
        if price_numeric < 5000:
            score += 20
            reasons.append("Budget-friendly flight")
        elif price_numeric < 10000:
            score += 15
            reasons.append("Reasonably priced")
        elif price_numeric < 20000:
            score += 10
            reasons.append("Premium pricing")

    # Direct flights get bonus points
    stops = flight_data.get("stops", "")
    if "non-stop" in stops.lower() or "0 stop" in stops.lower():
        score += 15
        reasons.append("Direct flight - saves time")

    # Shorter duration flights get bonus
    duration = flight_data.get("duration", "")
    if duration and "h" in duration:
        try:
            hours = int(duration.split("h")[0])
            if hours < 3:
                score += 10
                reasons.append("Short flight duration")
            elif hours < 6:
                score += 5
                reasons.append("Reasonable flight time")
        except:
            pass

    # Price history integration
    if price_history:
        flight_trend = price_history.get("flight_trend", {})
        if flight_trend.get("direction") == "decreasing":
            score += 15
            reasons.append("Flight prices trending down")
        elif flight_trend.get("direction") == "stable":
            score += 5
            reasons.append("Stable flight pricing")

    # Hotel availability coordination
    if hotel_data:
        score += 5
        reasons.append("Hotels available for destination")

    # Weather consideration (prefer flights when weather is good)
    if weather_data:
        temp = weather_data.get("temperature", 20)
        condition = weather_data.get("condition", "").lower()

        if 15 <= temp <= 28 and "sunny" in condition:
            score += 10
            reasons.append("Good weather expected at destination")
        elif temp < 10 or "rain" in condition:
            score += 5
            reasons.append("Consider weather when planning activities")

    return score, reasons