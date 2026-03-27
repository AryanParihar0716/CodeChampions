"""
Currency Agent — fetches current exchange rates for travel budgeting.
Uses ExchangeRate-API or similar to get real-time currency conversion rates.

This agent helps users understand costs in their preferred currency.
"""

import os
import requests
from typing import Dict, Any


def currency_node(state: dict) -> dict:
    """LangGraph node: fetches currency exchange rates."""
    user_prefs = state.get("user_preferences", {})
    preferred_currency = user_prefs.get("preferred_currency", "INR") if user_prefs else "INR"

    # Use ExchangeRate-API (free tier available)
    api_key = os.getenv("EXCHANGERATE_API_KEY")

    print(f"💱 Currency Agent: Getting exchange rates for {preferred_currency}...")

    try:
        # Get exchange rates
        rates = _get_exchange_rates(api_key)

        # Calculate conversions for common travel currencies
        conversions = {}
        base_currencies = ["USD", "EUR", "GBP", "JPY", "THB", "SGD", "AUD"]

        for currency in base_currencies:
            if currency in rates:
                conversions[currency] = {
                    "to_preferred": rates[currency],
                    "from_preferred": 1 / rates[currency] if rates[currency] != 0 else 0
                }

        # Get currency info for destination if available
        destination_currency = _get_destination_currency(state.get("destination", ""))

        return {
            "currency_result": {
                "preferred_currency": preferred_currency,
                "base_currency": "USD",  # API base
                "conversions": conversions,
                "destination_currency": destination_currency,
                "last_updated": rates.get("_last_updated", "")
            }
        }

    except Exception as e:
        print(f"⚠️ Currency agent failed: {e}")
        return {"currency_result": {"conversions": {}, "preferred_currency": preferred_currency}}


def _get_exchange_rates(api_key: str) -> Dict:
    """Fetch exchange rates from API."""
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    response = requests.get(url, timeout=10)
    data = response.json()

    if data.get("result") != "success":
        raise Exception("Exchange rate API failed")

    rates = data.get("conversion_rates", {})
    rates["_last_updated"] = data.get("time_last_update_utc", "")

    return rates


def _get_destination_currency(destination: str) -> Dict:
    """Get the primary currency for a destination country."""
    # Simplified mapping - in production, this could use a more comprehensive database
    currency_map = {
        "paris": {"code": "EUR", "name": "Euro", "symbol": "€"},
        "france": {"code": "EUR", "name": "Euro", "symbol": "€"},
        "london": {"code": "GBP", "name": "British Pound", "symbol": "£"},
        "uk": {"code": "GBP", "name": "British Pound", "symbol": "£"},
        "tokyo": {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
        "japan": {"code": "JPY", "name": "Japanese Yen", "symbol": "¥"},
        "bangkok": {"code": "THB", "name": "Thai Baht", "symbol": "฿"},
        "thailand": {"code": "THB", "name": "Thai Baht", "symbol": "฿"},
        "singapore": {"code": "SGD", "name": "Singapore Dollar", "symbol": "S$"},
        "dubai": {"code": "AED", "name": "UAE Dirham", "symbol": "د.إ"},
        "uae": {"code": "AED", "name": "UAE Dirham", "symbol": "د.إ"},
        "new york": {"code": "USD", "name": "US Dollar", "symbol": "$"},
        "usa": {"code": "USD", "name": "US Dollar", "symbol": "$"},
        "mumbai": {"code": "INR", "name": "Indian Rupee", "symbol": "₹"},
        "india": {"code": "INR", "name": "Indian Rupee", "symbol": "₹"}
    }

    # Try to match destination
    dest_lower = destination.lower()
    for key, currency in currency_map.items():
        if key in dest_lower:
            return currency

    # Default to USD if no match
    return {"code": "USD", "name": "US Dollar", "symbol": "$"}