"""
Reviews Agent — fetches user reviews and ratings for hotels/restaurants/attractions.
Uses Google Places API or similar for comprehensive review data.

This agent helps personalize recommendations by filtering options based on
user preferences and review scores.
"""

import os
import requests
from typing import List, Dict, Any


def reviews_node(state: dict) -> dict:
    """LangGraph node: fetches reviews for destination attractions/hotels."""
    destination = state.get("destination", "")
    user_prefs = state.get("user_preferences", {})

    # Use Google Places API (requires API key)
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY not set")
        return {"reviews_result": {"reviews": [], "average_rating": 0}}

    print(f"⭐ Reviews Agent: Fetching reviews for {destination}...")

    try:
        # First, search for places of interest in the destination
        places = _search_places(destination, api_key)

        # Get detailed reviews for top places
        reviews_data = []
        for place in places[:5]:  # Limit to top 5 places
            place_reviews = _get_place_reviews(place["place_id"], api_key)
            if place_reviews:
                reviews_data.extend(place_reviews)

        # Calculate average rating
        if reviews_data:
            avg_rating = sum(r.get("rating", 0) for r in reviews_data) / len(reviews_data)
        else:
            avg_rating = 0

        return {
            "reviews_result": {
                "reviews": reviews_data[:10],  # Return top 10 reviews
                "average_rating": round(avg_rating, 1),
                "total_reviews": len(reviews_data)
            }
        }

    except Exception as e:
        print(f"⚠️ Reviews agent failed: {e}")
        return {"reviews_result": {"reviews": [], "average_rating": 0}}


def _search_places(destination: str, api_key: str) -> List[Dict]:
    """Search for tourist attractions/hotels in destination."""
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    # Search for tourist attractions and hotels
    query = f"tourist attractions hotels restaurants in {destination}"

    params = {
        "query": query,
        "key": api_key,
        "language": "en",
        "type": "tourist_attraction|lodging|restaurant"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    places = []
    for result in data.get("results", []):
        places.append({
            "place_id": result.get("place_id"),
            "name": result.get("name"),
            "rating": result.get("rating", 0),
            "types": result.get("types", []),
            "address": result.get("formatted_address", "")
        })

    return places


def _get_place_reviews(place_id: str, api_key: str) -> List[Dict]:
    """Get detailed reviews for a specific place."""
    url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,
        "key": api_key,
        "fields": "reviews,name,rating",
        "language": "en"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    reviews = []
    place_info = data.get("result", {})

    for review in place_info.get("reviews", []):
        reviews.append({
            "place_name": place_info.get("name", ""),
            "author": review.get("author_name", "Anonymous"),
            "rating": review.get("rating", 0),
            "text": review.get("text", ""),
            "time": review.get("time", ""),
            "language": review.get("language", "en")
        })

    return reviews