"""
Events Agent — fetches local events, festivals, and seasonal activities.
Uses Eventbrite API or similar to get upcoming events in the destination.

This agent helps recommend travel timing based on events and activities.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any


def events_node(state: dict) -> dict:
    """LangGraph node: fetches events and activities for destination."""
    destination = state.get("destination", "")
    start_date = state.get("start_date")
    end_date = state.get("end_date")

    # Use Eventbrite API (requires API key)
    api_key = os.getenv("EVENTBRITE_API_KEY")

    if not api_key:
        print("❌ EVENTBRITE_API_KEY not set")
        return {"events_result": {"events": [], "seasonal_activities": []}}

    print(f"🎪 Events Agent: Finding events in {destination}...")

    try:
        # Get events for the destination and date range
        events = _search_events(destination, start_date, end_date, api_key)

        # Get seasonal activities (hardcoded for now, could be expanded)
        seasonal_activities = _get_seasonal_activities(destination, start_date)

        return {
            "events_result": {
                "events": events[:10],  # Top 10 events
                "seasonal_activities": seasonal_activities,
                "event_count": len(events)
            }
        }

    except Exception as e:
        print(f"⚠️ Events agent failed: {e}")
        return {"events_result": {"events": [], "seasonal_activities": []}}


def _search_events(destination: str, start_date: str, end_date: str, api_key: str) -> List[Dict]:
    """Search for events in destination using Eventbrite API."""
    url = "https://www.eventbriteapi.com/v3/events/search/"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # Convert dates to Eventbrite format
    start_datetime = f"{start_date}T00:00:00Z" if start_date else None
    end_datetime = f"{end_date}T23:59:59Z" if end_date else None

    params = {
        "q": destination,
        "location.address": destination,
        "start_date.range_start": start_datetime,
        "start_date.range_end": end_datetime,
        "categories": "103,113,116",  # Music, Food & Drink, Community
        "expand": "venue",
        "sort_by": "date"
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    data = response.json()

    events = []
    for event in data.get("events", []):
        venue = event.get("venue", {})

        events.append({
            "name": event.get("name", {}).get("text", ""),
            "description": event.get("description", {}).get("text", "")[:200] + "..." if event.get("description", {}).get("text") else "",
            "start_date": event.get("start", {}).get("local", ""),
            "end_date": event.get("end", {}).get("local", ""),
            "venue": venue.get("name", ""),
            "address": venue.get("address", {}).get("localized_address_display", ""),
            "url": event.get("url", ""),
            "category": event.get("category", {}).get("name", ""),
            "is_free": event.get("is_free", False)
        })

    return events


def _get_seasonal_activities(destination: str, start_date: str) -> List[Dict]:
    """Get seasonal activities and recommendations for the destination."""
    # This is a simplified version - in production, this could use more sophisticated data

    activities = []

    # Parse the month from start_date
    if start_date:
        try:
            month = datetime.strptime(start_date, "%Y-%m-%d").month
        except:
            month = datetime.now().month
    else:
        month = datetime.now().month

    # Seasonal recommendations based on destination and month
    seasonal_data = {
        "paris": {
            12: ["Christmas markets", "New Year's Eve celebrations", "Winter fashion shows"],
            4: ["Spring flower shows", "Paris Marathon", "Easter celebrations"],
            7: ["Bastille Day fireworks", "Summer music festivals", "Outdoor concerts"]
        },
        "tokyo": {
            3: ["Cherry blossom viewing", "Spring festivals", "Hanami parties"],
            8: ["Summer fireworks", "Beach festivals", "Mountain retreats"],
            12: ["Winter illuminations", "New Year's temple visits", "Ski trips nearby"]
        },
        "bangkok": {
            11: ["Loy Krathong festival", "Flower festivals", "Cooler weather activities"],
            4: ["Songkran water festival", "Traditional ceremonies", "Cultural performances"],
            12: ["New Year's celebrations", "Shopping festivals", "Holiday markets"]
        }
    }

    # Default activities for any destination
    default_activities = {
        12: ["Holiday markets", "Winter festivals", "New Year's events"],
        1: ["Winter sports", "Indoor activities", "Cultural exhibitions"],
        4: ["Spring festivals", "Outdoor activities", "Garden tours"],
        7: ["Summer festivals", "Beach activities", "Outdoor concerts"],
        10: ["Fall foliage", "Harvest festivals", "Cultural events"]
    }

    dest_key = destination.lower().replace(" ", "")
    seasonal_activities = seasonal_data.get(dest_key, {}).get(month, [])
    default_acts = default_activities.get(month, ["Local sightseeing", "Cultural experiences"])

    # Combine seasonal and default activities
    all_activities = seasonal_activities + default_acts

    for activity in all_activities[:5]:  # Limit to 5 activities
        activities.append({
            "name": activity,
            "type": "seasonal",
            "month": month,
            "recommended": True
        })

    return activities