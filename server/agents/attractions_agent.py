"""
Attractions Agent — fetches local attractions, restaurants, and points of interest.
Uses Google Places API or similar to get recommendations for activities and dining.

This agent provides personalized activity suggestions based on user preferences.
"""

import os
import requests
from typing import List, Dict, Any


def attractions_node(state: dict) -> dict:
    """LangGraph node: fetches attractions and dining options for destination."""
    destination = state.get("destination", "")
    user_prefs = state.get("user_prefs", {})

    # Use Google Places API
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY not set")
        return {"attractions_result": {"attractions": [], "restaurants": []}}

    print(f"🏛️ Attractions Agent: Finding activities in {destination}...")

    try:
        # Cross-agent data integration
        weather_data = state.get("weather_result", {})
        events_data = state.get("events_result", {})

        # Extract user preferences for filtering
        budget_max = user_prefs.get("budget_range", {}).get("max")
        dietary_restrictions = user_prefs.get("dietary_restrictions", [])
        activity_preferences = user_prefs.get("activity_preferences", [])
        accessibility_needs = user_prefs.get("accessibility_needs", [])
        group_size = user_prefs.get("group_size", 1)

        # Weather-influenced activity recommendations
        weather_based_activities = _get_weather_based_activities(weather_data)

        # Get top attractions with preference filtering
        attractions = _get_attractions(destination, api_key, budget_max, activity_preferences,
                                    accessibility_needs, group_size, weather_based_activities)

        # Get restaurant recommendations based on user preferences
        restaurants = _get_restaurants(destination, api_key, dietary_restrictions, budget_max,
                                     group_size, events_data)

        # Cross-reference with events for combined recommendations
        combined_recommendations = _combine_with_events(attractions, events_data)

        return {
            "attractions_result": {
                "attractions": attractions[:10],  # Top 10 attractions
                "restaurants": restaurants[:8],   # Top 8 restaurants
                "destination": destination,
                "weather_influenced": bool(weather_based_activities),
                "event_combinations": combined_recommendations
            }
        }

    except Exception as e:
        print(f"⚠️ Attractions agent failed: {e}")
        return {"attractions_result": {"attractions": [], "restaurants": []}}


def _get_attractions(destination: str, api_key: str, budget_max: float = None,
                    activity_preferences: List[str] = None, accessibility_needs: List[str] = None,
                    group_size: int = 1, weather_activities: List[str] = None) -> List[Dict]:
    """Get top attractions for the destination with preference filtering."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    # Search for tourist attractions
    query = f"tourist attractions landmarks museums in {destination}"

    # Add weather-based activities to query
    if weather_activities:
        query += f" {' '.join(weather_activities[:3])}"  # Add top 3 weather activities

    # Add activity preferences to query
    if activity_preferences:
        activity_keywords = {
            "adventure": "adventure outdoor hiking",
            "cultural": "museum historical cultural",
            "nature": "park nature outdoor",
            "shopping": "shopping mall market",
            "nightlife": "nightlife bar club",
            "family": "family friendly amusement park",
            "romantic": "romantic scenic viewpoint"
        }
        activity_terms = []
        for pref in activity_preferences:
            if pref.lower() in activity_keywords:
                activity_terms.extend(activity_keywords[pref.lower()].split())
        if activity_terms:
            query += f" {' '.join(set(activity_terms))}"

    params = {
        "query": query,
        "key": api_key,
        "type": "tourist_attraction",
        "language": "en"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    attractions = []
    for result in data.get("results", []):
        name = result.get("name", "")
        rating = result.get("rating", 0)
        price_level = result.get("price_level", 0)
        types = result.get("types", [])

        # Apply preference filters
        include_attraction = True

        # Budget filtering (price_level is 0-4, higher = more expensive)
        if budget_max and price_level > 2:  # Filter out expensive attractions
            include_attraction = False

        # Rating filter - prefer higher rated places
        if rating < 3.5:  # Skip low-rated attractions
            include_attraction = False

        # Accessibility filtering (basic keyword matching)
        if accessibility_needs:
            name_lower = name.lower()
            accessibility_keywords = ["wheelchair", "accessible", "disabled", "ramp"]
            has_accessibility = any(keyword in name_lower for keyword in accessibility_keywords)
            if not has_accessibility and "wheelchair" in accessibility_needs:
                include_attraction = False

        # Group size consideration (avoid very crowded places for large groups)
        if group_size > 6 and "crowded" in types:
            include_attraction = False

        if include_attraction:
            attractions.append({
                "name": name,
                "rating": rating,
                "address": result.get("formatted_address", ""),
                "types": types,
                "place_id": result.get("place_id", ""),
                "price_level": price_level,
                "user_ratings_total": result.get("user_ratings_total", 0)
            })

    return attractions


def _get_restaurants(destination: str, api_key: str, dietary_restrictions: List[str],
                    budget_max: float = None, group_size: int = 1, events_data: dict = None) -> List[Dict]:
    """Get restaurant recommendations considering dietary preferences and other filters."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    # Base query for restaurants
    query = f"restaurants in {destination}"

    # Add dietary preferences to query
    if dietary_restrictions:
        diet_keywords = {
            "vegetarian": "vegetarian",
            "vegan": "vegan",
            "halal": "halal",
            "kosher": "kosher",
            "gluten_free": "gluten free"
        }

        diet_terms = [diet_keywords.get(pref.lower(), pref) for pref in dietary_restrictions if pref.lower() in diet_keywords]
        if diet_terms:
            query += f" {' '.join(diet_terms)}"

    params = {
        "query": query,
        "key": api_key,
        "type": "restaurant",
        "language": "en"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    restaurants = []
    for result in data.get("results", []):
        name = result.get("name", "")
        rating = result.get("rating", 0)
        price_level = result.get("price_level", 0)
        types = result.get("types", [])

        # Apply preference filters
        include_restaurant = True

        # Budget filtering
        if budget_max and price_level > 2:  # Filter out expensive restaurants
            include_restaurant = False

        # Rating filter - prefer higher rated places
        if rating < 3.5:  # Skip low-rated restaurants
            include_restaurant = False

        # Group size consideration - prefer restaurants that can accommodate groups
        if group_size > 4:
            # Look for restaurant types that suggest they can handle groups
            group_friendly_types = ["restaurant", "food", "bar", "cafe"]
            if not any(t in types for t in group_friendly_types):
                include_restaurant = False

        if include_restaurant:
            restaurants.append({
                "name": name,
                "rating": rating,
                "address": result.get("formatted_address", ""),
                "price_level": price_level,
                "types": types,
                "user_ratings_total": result.get("user_ratings_total", 0),
                "place_id": result.get("place_id", "")
            })

    return restaurants


def _get_weather_based_activities(weather_data: dict) -> List[str]:
    """Get weather-influenced activity recommendations."""
    if not weather_data:
        return []

    activities = []
    temp = weather_data.get("temperature", 20)
    condition = weather_data.get("condition", "").lower()

    if temp > 25 and "sunny" in condition:
        activities.extend(["beach", "outdoor", "park", "hiking", "water_sports"])
    elif temp < 15:
        activities.extend(["museum", "indoor", "shopping", "spa", "theater"])
    elif "rain" in condition:
        activities.extend(["museum", "aquarium", "shopping", "spa", "indoor_attractions"])

    return activities


def _combine_with_events(attractions: List[Dict], events_data: dict) -> List[Dict]:
    """Combine attractions with events for comprehensive recommendations."""
    combinations = []

    if not events_data:
        return combinations

    events = events_data.get("events", [])
    if not events:
        return combinations

    # Create combinations of nearby attractions with events
    for event in events[:3]:  # Top 3 events
        event_name = event.get("name", "")
        event_date = event.get("date", "")

        # Find complementary attractions
        complementary = []
        for attraction in attractions[:5]:  # Check top attractions
            attr_name = attraction.get("name", "").lower()
            # Simple keyword matching for complementary activities
            if any(keyword in attr_name for keyword in ["museum", "park", "restaurant", "cafe"]):
                complementary.append(attraction.get("name"))

        if complementary:
            combinations.append({
                "event": event_name,
                "date": event_date,
                "complementary_attractions": complementary[:2],  # Top 2 complementary
                "combined_experience": f"Attend {event_name} and visit {', '.join(complementary[:2])}"
            })

    return combinations