"""
Price History Agent — tracks historical pricing for flights and hotels.
Uses Amadeus API or similar to get historical price data for trend analysis.

This agent enables price optimization and shows users if current prices are good deals.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any


def price_history_node(state: dict) -> dict:
    """LangGraph node: fetches historical price data for flights/hotels."""
    destination = state.get("destination", "")
    origin_city = state.get("origin_city", "Mumbai")
    start_date = state.get("start_date")

    # For now, we'll simulate price history since real historical APIs are expensive
    # In production, this would use Amadeus or similar APIs

    print(f"📊 Price History Agent: Analyzing price trends for {origin_city} to {destination}...")

    try:
        # Simulate historical price data
        flight_history = _get_simulated_flight_history(origin_city, destination, start_date)
        hotel_history = _get_simulated_hotel_history(destination, start_date)

        # Calculate price trends
        flight_trend = _calculate_price_trend(flight_history)
        hotel_trend = _calculate_price_trend(hotel_history)

        return {
            "price_history_result": {
                "flight_prices": flight_history,
                "hotel_prices": hotel_history,
                "flight_trend": flight_trend,
                "hotel_trend": hotel_trend,
                "recommendation": _generate_price_recommendation(flight_trend, hotel_trend)
            }
        }

    except Exception as e:
        print(f"⚠️ Price history agent failed: {e}")
        return {"price_history_result": {"flight_prices": [], "hotel_prices": []}}


def _get_simulated_flight_history(origin: str, destination: str, start_date: str) -> List[Dict]:
    """Simulate historical flight price data."""
    # In production, this would call a real API like Amadeus
    base_price = 8500  # Base price for the route

    history = []
    current_date = datetime.now()

    for days_back in range(30, 0, -1):  # Last 30 days
        date = current_date - timedelta(days=days_back)

        # Simulate price variation based on day of week and seasonality
        day_factor = 1.0 + (date.weekday() / 7.0) * 0.3  # Weekend premium
        seasonal_factor = 1.0 + abs(date.month - 6) * 0.1  # Peak in summer

        price = int(base_price * day_factor * seasonal_factor)
        price += (hash(date.strftime("%Y%m%d")) % 2000) - 1000  # Random variation

        history.append({
            "date": date.strftime("%Y-%m-%d"),
            "price": max(price, 3000),  # Minimum price
            "currency": "INR"
        })

    return history


def _get_simulated_hotel_history(destination: str, start_date: str) -> List[Dict]:
    """Simulate historical hotel price data."""
    base_price = 8000  # Base hotel price per night

    history = []
    current_date = datetime.now()

    for days_back in range(30, 0, -1):  # Last 30 days
        date = current_date - timedelta(days=days_back)

        # Simulate price variation
        occupancy_factor = 0.8 + (hash(date.strftime("%Y%m%d")) % 40) / 100.0  # 80-120%
        seasonal_factor = 1.0 + abs(date.month - 12) * 0.2  # Peak in December

        price = int(base_price * occupancy_factor * seasonal_factor)

        history.append({
            "date": date.strftime("%Y-%m-%d"),
            "price_per_night": max(price, 2000),  # Minimum price
            "currency": "INR"
        })

    return history


def _calculate_price_trend(price_history: List[Dict]) -> Dict:
    """Calculate price trend from historical data."""
    if not price_history:
        return {"direction": "stable", "change_percent": 0}

    prices = [item.get("price") or item.get("price_per_night", 0) for item in price_history]

    if len(prices) < 2:
        return {"direction": "stable", "change_percent": 0}

    # Compare recent average (last 7 days) vs earlier average (previous 7 days)
    recent_avg = sum(prices[-7:]) / len(prices[-7:])
    earlier_avg = sum(prices[-14:-7]) / len(prices[-14:-7]) if len(prices) >= 14 else recent_avg

    if earlier_avg == 0:
        return {"direction": "stable", "change_percent": 0}

    change_percent = ((recent_avg - earlier_avg) / earlier_avg) * 100

    if change_percent > 5:
        direction = "increasing"
    elif change_percent < -5:
        direction = "decreasing"
    else:
        direction = "stable"

    return {
        "direction": direction,
        "change_percent": round(change_percent, 1),
        "current_avg": round(recent_avg),
        "previous_avg": round(earlier_avg)
    }


def _generate_price_recommendation(flight_trend: Dict, hotel_trend: Dict) -> str:
    """Generate price-based recommendation."""
    flight_dir = flight_trend.get("direction", "stable")
    hotel_dir = hotel_trend.get("direction", "stable")

    if flight_dir == "decreasing" and hotel_dir == "decreasing":
        return "Great time to book! Both flight and hotel prices are trending down."
    elif flight_dir == "increasing" or hotel_dir == "increasing":
        return "Consider booking soon - prices are rising."
    else:
        return "Prices are stable. Book when convenient."