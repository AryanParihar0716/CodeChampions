"""
Hotel Search Agent — uses Sky Scrapper (Skyscanner) API via RapidAPI.
Searches for hotels at the destination city.
"""

import os
import requests


RAPIDAPI_HOST = "sky-scrapper.p.rapidapi.com"


def _search_destination(query: str, api_key: str) -> dict | None:
    """Look up a Skyscanner entity ID for a hotel destination."""
    url = f"https://{RAPIDAPI_HOST}/api/v1/hotels/searchDestination"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }
    params = {"query": query}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        data = res.json()
        entities = data.get("data", [])
        if entities:
            return entities[0]
    except Exception as e:
        print(f"⚠️ Hotel destination lookup failed for '{query}': {e}")
    return None


def hotel_node(state: dict) -> dict:
    """LangGraph node: searches for hotels via Sky Scrapper API with cross-agent integration."""
    city = state.get("destination", "")
    start_date = state.get("start_date")
    end_date = state.get("end_date")
    group_size = state.get("group_size", 2)  # Use user's group size
    user_prefs = state.get("user_prefs", {})
    api_key = os.getenv("RAPIDAPI_KEY")

    if not api_key:
        print("❌ RAPIDAPI_KEY not set")
        return {"hotel_result": {"hotels": []}}

    # Cross-agent data integration
    flight_data = state.get("flight_result", {}).get("flights", [])
    weather_data = state.get("weather_result", {})
    reviews_data = state.get("reviews_result", {})
    price_history = state.get("price_history_result", {})

    # Adjust dates based on flight information
    adjusted_start, adjusted_end = _adjust_dates_for_flights(start_date, end_date, flight_data)

    print(f"🏨 Hotel Agent: Searching hotels in {city} for {group_size} adults...")
    print(f"🏨 Booking dates: {adjusted_start} to {adjusted_end}")

    # Apply user preferences for filtering
    preferred_types = user_prefs.get("preferred_hotel_types", [])
    budget_min = user_prefs.get("budget_range", {}).get("min")
    budget_max = user_prefs.get("budget_range", {}).get("max")

    if preferred_types:
        print(f"🏨 Filtering by preferred hotel types: {preferred_types}")
    if budget_min or budget_max:
        print(f"🏨 Filtering by budget: ₹{budget_min or 0} - ₹{budget_max or 'unlimited'}")

    # Weather-based recommendations
    weather_adjustments = _get_weather_adjustments(weather_data)
    if weather_adjustments:
        print(f"🏨 Weather considerations: {weather_adjustments}")

    # Step 1: Resolve destination entity
    dest = _search_destination(city, api_key)

    if not dest:
        print(f"❌ Could not resolve hotel destination: {city}")
        return {"hotel_result": {"hotels": []}}

    entity_id = dest.get("entityId", "")

    # Step 2: Search hotels
    url = f"https://{RAPIDAPI_HOST}/api/v1/hotels/searchHotels"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }
    params = {
        "entityId": entity_id,
        "checkin": adjusted_start or "",
        "checkout": adjusted_end or "",
        "adults": str(group_size),
        "currency": "INR",
    }

    try:
        res = requests.get(url, headers=headers, params=params, timeout=15)
        data = res.json()

        raw_hotels = data.get("data", {}).get("hotels", [])
        hotels = []

        for h in raw_hotels[:10]:  # Get more results to allow filtering
            name = h.get("name", "Unknown Hotel")
            price = h.get("price", "N/A")

            # Extract numeric price for filtering
            price_numeric = None
            if isinstance(price, str) and "₹" in price:
                try:
                    price_numeric = float(price.replace("₹", "").replace(",", ""))
                except:
                    pass
            elif isinstance(price, (int, float)):
                price_numeric = float(price)

            stars = h.get("stars", 0)
            image = ""
            images = h.get("images", [])
            if images:
                image = images[0] if isinstance(images[0], str) else images[0].get("url", "")

            # Some API versions use different structures
            hero_image = h.get("heroImage", "")
            if not image and hero_image:
                image = hero_image

            hotel_data = {
                "name": name,
                "price": price,
                "price_numeric": price_numeric,
                "image": image,
                "stars": stars,
                "cross_agent_score": 0,  # Score for cross-agent recommendations
                "recommendation_reasons": []
            }

            # Apply user preference filters
            include_hotel = True

            # Budget filtering
            if budget_min and price_numeric and price_numeric < budget_min:
                include_hotel = False
            if budget_max and price_numeric and price_numeric > budget_max:
                include_hotel = False

            # Hotel type filtering (basic keyword matching)
            if preferred_types:
                hotel_name_lower = name.lower()
                type_match = any(hotel_type.lower() in hotel_name_lower for hotel_type in preferred_types)
                if not type_match:
                    # Check star rating as fallback
                    if "luxury" in preferred_types and stars >= 4:
                        type_match = True
                        hotel_data["recommendation_reasons"].append("Matches luxury preference")
                    elif "budget" in preferred_types and stars <= 3:
                        type_match = True
                        hotel_data["recommendation_reasons"].append("Budget-friendly option")
                    elif "boutique" in preferred_types and stars == 3:
                        type_match = True
                        hotel_data["recommendation_reasons"].append("Boutique-style hotel")

                if not type_match:
                    include_hotel = False

            # Cross-agent filtering and scoring
            if include_hotel:
                cross_score, reasons = _calculate_cross_agent_score(
                    hotel_data, reviews_data, price_history, weather_adjustments, flight_data
                )
                hotel_data["cross_agent_score"] = cross_score
                hotel_data["recommendation_reasons"].extend(reasons)

                hotels.append(hotel_data)

        # Sort by cross-agent score and limit to top 5
        hotels.sort(key=lambda x: x["cross_agent_score"], reverse=True)
        hotels = hotels[:5]

        print(f"✅ Found {len(hotels)} hotels in {city} (with cross-agent scoring)")
        return {"hotel_result": {"hotels": hotels}}

    except Exception as e:
        print(f"❌ Hotel search error: {e}")
        return {"hotel_result": {"hotels": []}}


def _adjust_dates_for_flights(start_date: str, end_date: str, flight_data: list) -> tuple:
    """Adjust hotel booking dates based on flight information."""
    if not flight_data:
        return start_date, end_date

    # For now, return original dates - could be enhanced to adjust based on flight times
    # This is a placeholder for more sophisticated flight-hotel coordination
    return start_date, end_date


def _get_weather_adjustments(weather_data: dict) -> list:
    """Get weather-based adjustments for hotel recommendations."""
    if not weather_data:
        return []

    adjustments = []
    temp = weather_data.get("temperature", 20)
    condition = weather_data.get("condition", "").lower()

    if temp > 30:
        adjustments.append("air_conditioning_priority")
    elif temp < 15:
        adjustments.append("heating_priority")

    if "rain" in condition:
        adjustments.append("indoor_facilities")
    elif "sunny" in condition:
        adjustments.append("pool_outdoor_access")

    return adjustments


def _calculate_cross_agent_score(hotel_data: dict, reviews_data: dict,
                               price_history: dict, weather_adjustments: list,
                               flight_data: list) -> tuple:
    """Calculate a cross-agent recommendation score for the hotel."""
    score = 0
    reasons = []

    # Base score from star rating
    stars = hotel_data.get("stars", 0)
    score += stars * 10  # 0-50 points from stars

    # Reviews integration
    if reviews_data:
        avg_rating = reviews_data.get("average_rating", 0)
        if avg_rating >= 4.0:
            score += 20
            reasons.append(f"Highly rated ({avg_rating}/5 stars)")
        elif avg_rating >= 3.0:
            score += 10
            reasons.append(f"Well rated ({avg_rating}/5 stars)")

    # Price history integration
    if price_history:
        hotel_trend = price_history.get("hotel_trend", {})
        if hotel_trend.get("direction") == "decreasing":
            score += 15
            reasons.append("Prices trending down - good time to book")
        elif hotel_trend.get("direction") == "stable":
            score += 5
            reasons.append("Stable pricing")

    # Weather-based scoring
    hotel_name = hotel_data.get("name", "").lower()
    if weather_adjustments:
        if "air_conditioning_priority" in weather_adjustments and "ac" in hotel_name:
            score += 10
            reasons.append("Good for hot weather")
        if "pool_outdoor_access" in weather_adjustments and ("pool" in hotel_name or "resort" in hotel_name):
            score += 10
            reasons.append("Outdoor facilities for good weather")

    # Flight coordination (placeholder for future enhancement)
    if flight_data:
        score += 5  # Small boost for having flight data available
        reasons.append("Coordinates with available flights")

    return score, reasons
