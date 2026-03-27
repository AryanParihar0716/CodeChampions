"""
Transportation Agent — fetches local transportation options and costs.
Uses Google Maps API or similar to get transport information for the destination.

This agent helps users plan local travel within their destination.
"""

import os
import requests
from typing import List, Dict, Any


def transport_node(state: dict) -> dict:
    """LangGraph node: fetches transportation options for destination."""
    destination = state.get("destination", "")

    # Use Google Maps API for transportation data
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not api_key:
        print("❌ GOOGLE_MAPS_API_KEY not set")
        return {"transport_result": {"options": [], "costs": {}}}

    print(f"🚗 Transportation Agent: Getting transport options for {destination}...")

    try:
        # Get transportation options for the destination
        transport_options = _get_transport_options(destination, api_key)

        # Get estimated costs
        transport_costs = _get_transport_costs(destination)

        return {
            "transport_result": {
                "options": transport_options,
                "estimated_costs": transport_costs,
                "destination": destination
            }
        }

    except Exception as e:
        print(f"⚠️ Transportation agent failed: {e}")
        return {"transport_result": {"options": [], "costs": {}}}


def _get_transport_options(destination: str, api_key: str) -> List[Dict]:
    """Get available transportation options in the destination."""
    # This is a simplified version - in production, would use Google Places API
    # to find transport services, stations, etc.

    # Common transport options by destination type
    transport_data = {
        "paris": [
            {"type": "Metro", "name": "Paris Métro", "coverage": "City-wide", "frequency": "Every 2-5 minutes"},
            {"type": "Bus", "name": "RATP Bus", "coverage": "City-wide", "frequency": "Every 5-15 minutes"},
            {"type": "Train", "name": "RER", "coverage": "Suburban", "frequency": "Every 3-10 minutes"},
            {"type": "Bike", "name": "Vélib'", "coverage": "City center", "frequency": "24/7"},
            {"type": "Taxi", "name": "Taxis", "coverage": "City-wide", "frequency": "On-demand"}
        ],
        "tokyo": [
            {"type": "Train", "name": "JR Lines", "coverage": "City-wide", "frequency": "Every 2-5 minutes"},
            {"type": "Subway", "name": "Tokyo Metro", "coverage": "Central Tokyo", "frequency": "Every 3-7 minutes"},
            {"type": "Bus", "name": "Toei Bus", "coverage": "City-wide", "frequency": "Every 5-20 minutes"},
            {"type": "Taxi", "name": "Taxi", "coverage": "City-wide", "frequency": "On-demand"}
        ],
        "bangkok": [
            {"type": "BTS", "name": "Skytrain", "coverage": "Central Bangkok", "frequency": "Every 3-6 minutes"},
            {"type": "MRT", "name": "Subway", "coverage": "Central Bangkok", "frequency": "Every 4-8 minutes"},
            {"type": "Boat", "name": "Chao Phraya Express", "coverage": "River routes", "frequency": "Every 15-30 minutes"},
            {"type": "Taxi", "name": "Taxi/Metered", "coverage": "City-wide", "frequency": "On-demand"},
            {"type": "Grab/Bolt", "name": "Ride-hailing", "coverage": "City-wide", "frequency": "On-demand"}
        ],
        "london": [
            {"type": "Tube", "name": "London Underground", "coverage": "City-wide", "frequency": "Every 2-8 minutes"},
            {"type": "Bus", "name": "London Buses", "coverage": "City-wide", "frequency": "Every 2-10 minutes"},
            {"type": "Train", "name": "Overground", "coverage": "Suburban", "frequency": "Every 3-15 minutes"},
            {"type": "Taxi", "name": "Black Cabs", "coverage": "City-wide", "frequency": "On-demand"}
        ]
    }

    # Try to match destination
    dest_key = destination.lower().replace(" ", "")
    for key, options in transport_data.items():
        if key in dest_key:
            return options

    # Default transport options for any city
    return [
        {"type": "Bus", "name": "Local Buses", "coverage": "City-wide", "frequency": "Every 10-30 minutes"},
        {"type": "Taxi", "name": "Taxis", "coverage": "City-wide", "frequency": "On-demand"},
        {"type": "Ride-hailing", "name": "Uber/Grab/etc", "coverage": "City-wide", "frequency": "On-demand"},
        {"type": "Train/Subway", "name": "Public Transit", "coverage": "Central areas", "frequency": "Every 5-15 minutes"}
    ]


def _get_transport_costs(destination: str) -> Dict:
    """Get estimated transportation costs for the destination."""
    # Estimated costs in USD (would be converted to user's currency)
    cost_data = {
        "paris": {
            "metro_single": 2.10,
            "taxi_per_km": 1.05,
            "bus_single": 2.10,
            "bike_rental_hourly": 1.70,
            "uber_base": 4.10
        },
        "tokyo": {
            "train_single": 1.50,
            "subway_single": 1.50,
            "taxi_per_km": 2.00,
            "bus_single": 1.20
        },
        "bangkok": {
            "bts_single": 0.35,
            "mrt_single": 0.45,
            "taxi_per_km": 0.30,
            "boat_single": 0.25,
            "grab_base": 1.00
        },
        "london": {
            "tube_single": 3.20,
            "bus_single": 1.75,
            "taxi_per_km": 2.50,
            "uber_base": 3.00
        }
    }

    # Try to match destination
    dest_key = destination.lower().replace(" ", "")
    for key, costs in cost_data.items():
        if key in dest_key:
            return costs

    # Default costs
    return {
        "bus_single": 1.00,
        "taxi_per_km": 1.00,
        "ride_hailing_base": 2.00,
        "public_transit_single": 1.50
    }