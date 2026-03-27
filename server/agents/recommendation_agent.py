"""
Recommendation Engine Agent — analyzes user history and multiple data sources
to generate personalized travel recommendations and complete itineraries.

This agent provides intelligent suggestions based on:
- User search history and preferences
- Cross-referenced data from multiple sources
- Predictive recommendations based on patterns
- Complete travel itinerary generation
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db_session, User, SearchHistory, UserPreferences


def recommendation_node(state: dict) -> dict:
    """LangGraph node: generates personalized travel recommendations and itineraries."""
    user_id = state.get("user_id")
    destination = state.get("destination", "")
    user_prefs = state.get("user_prefs", {})

    if not user_id:
        print("❌ No user ID provided for recommendations")
        return {"recommendation_result": {"recommendations": [], "itinerary": None}}

    print(f"🧠 Recommendation Engine: Analyzing data for user {user_id}...")

    try:
        # Get user history and preferences
        user_history = _get_user_history(user_id)
        user_profile = _get_user_profile(user_id)

        # Analyze patterns and generate recommendations
        recommendations = _generate_recommendations(
            user_history, user_profile, destination, state
        )

        # Generate complete itinerary if destination is specified
        itinerary = None
        if destination:
            itinerary = _generate_itinerary(destination, state, user_profile)

        return {
            "recommendation_result": {
                "recommendations": recommendations,
                "itinerary": itinerary,
                "user_insights": _extract_user_insights(user_history, user_profile)
            }
        }

    except Exception as e:
        print(f"❌ Recommendation engine failed: {e}")
        return {"recommendation_result": {"recommendations": [], "itinerary": None}}


def _get_user_history(user_id: int) -> List[Dict]:
    """Retrieve user's search history for pattern analysis."""
    session = get_db_session()
    try:
        history_records = session.query(SearchHistory).filter_by(user_id=user_id).all()
        history = []
        for record in history_records:
            history.append({
                "query": record.query,
                "destination": record.destination,
                "timestamp": record.search_date.isoformat() if record.search_date else None,
                "results_count": record.results_summary.get("has_flights", 0) + record.results_summary.get("has_hotels", 0) if record.results_summary else 0
            })
        return history
    finally:
        session.close()


def _get_user_profile(user_id: int) -> Dict:
    """Get user's preferences and profile data."""
    session = get_db_session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return {}

        # Get all user preferences from UserPreferences table
        all_prefs = session.query(UserPreferences).filter_by(user_id=user_id).all()

        # Organize preferences by category
        preferences = {
            "origin_city": user.origin_city,
            "budget_range": {
                "min": user.budget_range_min,
                "max": user.budget_range_max
            },
            "travel_style": user.travel_style,
            "group_size": user.group_size,
            "preferred_airlines": user.preferred_airlines or [],
            "preferred_hotel_types": user.preferred_hotel_types or [],
            "dietary_restrictions": user.dietary_restrictions or [],
            "activity_preferences": [],
            "accessibility_needs": user.accessibility_needs or [],
            "destinations": [],
            "seasons": []
        }

        # Add preferences from UserPreferences table
        for pref in all_prefs:
            if pref.category == "activities":
                preferences["activity_preferences"].append({
                    "item": pref.item,
                    "score": pref.preference_score
                })
            elif pref.category == "destinations":
                preferences["destinations"].append({
                    "item": pref.item,
                    "score": pref.preference_score
                })
            elif pref.category == "seasons":
                preferences["seasons"].append({
                    "item": pref.item,
                    "score": pref.preference_score
                })

        profile = {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "preferences": preferences
        }

        return profile
    finally:
        session.close()


def _generate_recommendations(user_history: List[Dict], user_profile: Dict,
                            destination: str, state: dict) -> List[Dict]:
    """Generate personalized recommendations based on user data."""
    recommendations = []

    # Extract patterns from history
    destinations = [h["destination"] for h in user_history if h["destination"]]
    search_patterns = _analyze_search_patterns(user_history)

    # Cross-reference with current data
    flight_data = state.get("flight_result", {}).get("flights", [])
    hotel_data = state.get("hotel_result", {}).get("hotels", [])
    weather_data = state.get("weather_result", {})
    attractions_data = state.get("attractions_result", {})

    # Generate destination recommendations
    if not destination:
        dest_recs = _recommend_destinations(destinations, search_patterns, user_profile)
        recommendations.extend(dest_recs)

    # Generate timing recommendations
    timing_recs = _recommend_timing(weather_data, search_patterns)
    recommendations.extend(timing_recs)

    # Generate budget optimization recommendations
    budget_recs = _recommend_budget_optimization(flight_data, hotel_data, user_profile)
    recommendations.extend(budget_recs)

    # Generate activity recommendations
    activity_recs = _recommend_activities(attractions_data, user_profile)
    recommendations.extend(activity_recs)

    return recommendations[:10]  # Top 10 recommendations


def _analyze_search_patterns(history: List[Dict]) -> Dict:
    """Analyze user search patterns for insights."""
    patterns = {
        "frequent_destinations": {},
        "preferred_months": {},
        "budget_patterns": [],
        "group_sizes": {},
        "search_frequency": len(history)
    }

    for record in history:
        # Destination frequency
        dest = record.get("destination", "")
        if dest:
            patterns["frequent_destinations"][dest] = patterns["frequent_destinations"].get(dest, 0) + 1

        # Month preferences
        timestamp = record.get("timestamp")
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                month = dt.strftime("%B")
                patterns["preferred_months"][month] = patterns["preferred_months"].get(month, 0) + 1
            except:
                pass

    return patterns


def _recommend_destinations(destinations: List[str], patterns: Dict, user_profile: Dict) -> List[Dict]:
    """Recommend destinations based on user patterns."""
    recommendations = []

    # Based on frequency
    freq_dests = patterns.get("frequent_destinations", {})
    for dest, count in sorted(freq_dests.items(), key=lambda x: x[1], reverse=True)[:3]:
        recommendations.append({
            "type": "destination",
            "title": f"Return to {dest}",
            "description": f"You've searched for {dest} {count} times. Consider booking your next trip there.",
            "confidence": min(count * 20, 100),  # Confidence based on frequency
            "reason": "based_on_search_history"
        })

    # Based on preferences
    prefs = user_profile.get("preferences", {})
    travel_style = prefs.get("travel_style", "").lower()

    if travel_style == "adventure":
        recommendations.append({
            "type": "destination",
            "title": "Adventure Destination: Nepal",
            "description": "Based on your adventure travel style, consider trekking in Nepal.",
            "confidence": 85,
            "reason": "based_on_travel_style"
        })
    elif travel_style == "cultural":
        recommendations.append({
            "type": "destination",
            "title": "Cultural Destination: Kyoto, Japan",
            "description": "Explore ancient temples and traditions in Kyoto.",
            "confidence": 80,
            "reason": "based_on_travel_style"
        })

    return recommendations


def _recommend_timing(weather_data: Dict, patterns: Dict) -> List[Dict]:
    """Recommend optimal timing based on weather and patterns."""
    recommendations = []

    # Weather-based timing
    if weather_data:
        temp = weather_data.get("temperature", 0)
        condition = weather_data.get("condition", "").lower()

        if temp < 15:
            recommendations.append({
                "type": "timing",
                "title": "Consider Warmer Months",
                "description": f"Current temperature is {temp}°C. You might prefer traveling during warmer months.",
                "confidence": 75,
                "reason": "weather_based"
            })
        elif "rain" in condition:
            recommendations.append({
                "type": "timing",
                "title": "Rainy Season Alert",
                "description": "Current weather shows rain. Consider indoor activities or different timing.",
                "confidence": 70,
                "reason": "weather_based"
            })

    # Pattern-based timing
    preferred_months = patterns.get("preferred_months", {})
    if preferred_months:
        top_month = max(preferred_months.items(), key=lambda x: x[1])[0]
        recommendations.append({
            "type": "timing",
            "title": f"Preferred Travel Month: {top_month}",
            "description": f"You've searched most frequently in {top_month}. This might be your preferred travel time.",
            "confidence": 65,
            "reason": "pattern_based"
        })

    return recommendations


def _recommend_budget_optimization(flights: List[Dict], hotels: List[Dict], user_profile: Dict) -> List[Dict]:
    """Recommend budget optimization strategies."""
    recommendations = []

    prefs = user_profile.get("preferences", {})
    budget_max = prefs.get("budget_range", {}).get("max")

    if flights and budget_max:
        # Find cheapest flight
        sorted_flights = sorted(flights, key=lambda x: _extract_price(x.get("price", "0")))
        if sorted_flights:
            cheapest = sorted_flights[0]
            price = cheapest.get("price", "N/A")
            recommendations.append({
                "type": "budget",
                "title": f"Budget Flight Option: {price}",
                "description": f"Consider this economical flight option with {cheapest.get('airline', 'Unknown')}.",
                "confidence": 80,
                "reason": "price_comparison"
            })

    if hotels and budget_max:
        # Find budget-friendly hotels
        budget_hotels = [h for h in hotels if _extract_price(h.get("price", "0")) <= budget_max * 0.7]
        if budget_hotels:
            recommendations.append({
                "type": "budget",
                "title": "Budget Hotel Options Available",
                "description": f"Found {len(budget_hotels)} hotels within 70% of your budget range.",
                "confidence": 75,
                "reason": "budget_optimization"
            })

    return recommendations


def _recommend_activities(attractions_data: Dict, user_profile: Dict) -> List[Dict]:
    """Recommend activities based on user preferences."""
    recommendations = []

    attractions = attractions_data.get("attractions", [])
    restaurants = attractions_data.get("restaurants", [])

    prefs = user_profile.get("preferences", {})
    dietary_restrictions = prefs.get("dietary_restrictions", [])
    activity_preferences = prefs.get("activity_preferences", [])

    # Restaurant recommendations based on dietary needs
    if dietary_restrictions and restaurants:
        diet_friendly = [r for r in restaurants if any(d.lower() in str(r).lower() for d in dietary_restrictions)]
        if diet_friendly:
            recommendations.append({
                "type": "activity",
                "title": f"Dietary-Friendly Restaurants ({len(diet_friendly)} found)",
                "description": f"Found restaurants accommodating your {', '.join(dietary_restrictions)} preferences.",
                "confidence": 90,
                "reason": "dietary_preferences"
            })

    # Activity recommendations based on preferences
    if activity_preferences and attractions:
        matching_activities = []
        for pref in activity_preferences:
            pref_lower = pref.lower()
            for attraction in attractions:
                name_lower = attraction.get("name", "").lower()
                types = [t.lower() for t in attraction.get("types", [])]
                if pref_lower in name_lower or any(pref_lower in t for t in types):
                    matching_activities.append(attraction.get("name"))

        if matching_activities:
            recommendations.append({
                "type": "activity",
                "title": f"Preferred Activities Available",
                "description": f"Found {len(set(matching_activities))} activities matching your {', '.join(activity_preferences)} preferences.",
                "confidence": 85,
                "reason": "activity_preferences"
            })

    return recommendations


def _generate_itinerary(destination: str, state: dict, user_profile: Dict) -> Dict:
    """Generate a complete travel itinerary."""
    itinerary = {
        "destination": destination,
        "duration": "3-5 days",  # Default
        "days": []
    }

    # Extract data from various agents
    flights = state.get("flight_result", {}).get("flights", [])
    hotels = state.get("hotel_result", {}).get("hotels", [])
    attractions = state.get("attractions_result", {}).get("attractions", [])
    restaurants = state.get("attractions_result", {}).get("restaurants", [])
    weather = state.get("weather_result", {})
    events = state.get("events_result", {}).get("events", [])

    # Build day-by-day itinerary
    days = []

    # Day 1: Arrival and local exploration
    day1 = {
        "day": 1,
        "theme": "Arrival & Exploration",
        "activities": []
    }

    if flights:
        day1["activities"].append({
            "type": "transport",
            "title": f"Arrive via {flights[0].get('airline', 'Flight')}",
            "details": f"Duration: {flights[0].get('duration', 'N/A')}"
        })

    if hotels:
        day1["activities"].append({
            "type": "accommodation",
            "title": f"Check into {hotels[0].get('name', 'Hotel')}",
            "details": f"Price: {hotels[0].get('price', 'N/A')}"
        })

    if attractions:
        day1["activities"].append({
            "type": "attraction",
            "title": f"Visit {attractions[0].get('name', 'Local Attraction')}",
            "details": f"Rating: {attractions[0].get('rating', 'N/A')}/5"
        })

    days.append(day1)

    # Day 2: Main activities
    day2 = {
        "day": 2,
        "theme": "Main Activities",
        "activities": []
    }

    if len(attractions) > 1:
        day2["activities"].append({
            "type": "attraction",
            "title": f"Explore {attractions[1].get('name', 'Another Attraction')}",
            "details": f"Address: {attractions[1].get('address', 'N/A')}"
        })

    if events:
        day2["activities"].append({
            "type": "event",
            "title": f"Attend {events[0].get('name', 'Local Event')}",
            "details": f"Date: {events[0].get('date', 'N/A')}"
        })

    if restaurants:
        day2["activities"].append({
            "type": "dining",
            "title": f"Dine at {restaurants[0].get('name', 'Restaurant')}",
            "details": f"Rating: {restaurants[0].get('rating', 'N/A')}/5"
        })

    days.append(day2)

    # Day 3: Leisure and departure prep
    day3 = {
        "day": 3,
        "theme": "Leisure & Departure",
        "activities": []
    }

    if len(restaurants) > 1:
        day3["activities"].append({
            "type": "dining",
            "title": f"Try {restaurants[1].get('name', 'Another Restaurant')}",
            "details": "Local cuisine experience"
        })

    day3["activities"].append({
        "type": "transport",
        "title": "Departure Day",
        "details": "Prepare for your journey home"
    })

    days.append(day3)

    itinerary["days"] = days
    return itinerary


def _extract_user_insights(history: List[Dict], profile: Dict) -> Dict:
    """Extract key insights about user travel behavior."""
    insights = {
        "total_searches": len(history),
        "preferred_destinations": [],
        "travel_frequency": "occasional",
        "budget_category": "medium",
        "travel_style": profile.get("preferences", {}).get("travel_style", "general")
    }

    # Analyze destinations
    destinations = {}
    for record in history:
        dest = record.get("destination")
        if dest:
            destinations[dest] = destinations.get(dest, 0) + 1

    insights["preferred_destinations"] = sorted(destinations.items(), key=lambda x: x[1], reverse=True)[:3]

    # Determine travel frequency
    if len(history) > 20:
        insights["travel_frequency"] = "frequent"
    elif len(history) > 10:
        insights["travel_frequency"] = "regular"
    else:
        insights["travel_frequency"] = "occasional"

    # Determine budget category
    budget_max = profile.get("preferences", {}).get("budget_range", {}).get("max", 0)
    if budget_max > 50000:
        insights["budget_category"] = "luxury"
    elif budget_max > 20000:
        insights["budget_category"] = "premium"
    elif budget_max > 10000:
        insights["budget_category"] = "medium"
    else:
        insights["budget_category"] = "budget"

    return insights


def _extract_price(price_str: str) -> float:
    """Extract numeric price from price string."""
    if isinstance(price_str, (int, float)):
        return float(price_str)

    import re
    # Extract numbers from strings like "₹3,500" or "$250"
    numbers = re.findall(r'[\d,]+', str(price_str))
    if numbers:
        return float(numbers[0].replace(',', ''))
    return 0