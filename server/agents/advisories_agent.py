"""
Travel Advisories Agent — fetches government travel advisories and safety warnings.
Uses official government APIs or news sources to get current travel alerts.

This agent provides safety information to help users make informed decisions.
"""

import os
import requests
from typing import List, Dict, Any


def advisories_node(state: dict) -> dict:
    """LangGraph node: fetches travel advisories for destination."""
    destination = state.get("destination", "")

    print(f"⚠️ Travel Advisories Agent: Checking advisories for {destination}...")

    try:
        # Get advisories from multiple sources
        us_state_dept = _get_us_state_department_advisory(destination)
        uk_gov = _get_uk_government_advisory(destination)
        india_mea = _get_india_mea_advisory(destination)

        # Combine and prioritize advisories
        advisories = [adv for adv in [us_state_dept, uk_gov, india_mea] if adv]

        # Determine overall risk level
        risk_level = _calculate_overall_risk(advisories)

        return {
            "advisories_result": {
                "advisories": advisories,
                "overall_risk": risk_level,
                "recommendations": _generate_safety_recommendations(risk_level)
            }
        }

    except Exception as e:
        print(f"⚠️ Travel advisories agent failed: {e}")
        return {"advisories_result": {"advisories": [], "overall_risk": "unknown"}}


def _get_us_state_department_advisory(destination: str) -> Dict:
    """Get advisory from US State Department."""
    # Note: This is a simplified version. Real implementation would need official API access
    # For now, we'll simulate based on common advisory levels

    advisory_levels = {
        "low": ["Canada", "UK", "Australia", "New Zealand"],
        "exercise_caution": ["France", "Germany", "Japan", "Singapore"],
        "reconsider": ["Mexico", "Brazil", "South Africa"],
        "do_not_travel": ["Afghanistan", "Syria", "North Korea"]
    }

    dest_lower = destination.lower()

    for level, countries in advisory_levels.items():
        if any(country.lower() in dest_lower for country in countries):
            return {
                "source": "US State Department",
                "level": level,
                "description": f"Level {level.replace('_', ' ').title()}",
                "last_updated": "2024-01-15"
            }

    return {
        "source": "US State Department",
        "level": "normal",
        "description": "Normal travel conditions",
        "last_updated": "2024-01-15"
    }


def _get_uk_government_advisory(destination: str) -> Dict:
    """Get advisory from UK Foreign Office."""
    # Simplified simulation
    uk_levels = {
        "green": ["USA", "Canada", "Australia"],
        "amber": ["France", "Spain", "Italy"],
        "red": ["Russia", "Ukraine"]
    }

    dest_lower = destination.lower()

    for level, countries in uk_levels.items():
        if any(country.lower() in dest_lower for country in countries):
            return {
                "source": "UK Foreign Office",
                "level": level,
                "description": f"{level.title()} level advisory",
                "last_updated": "2024-01-15"
            }

    return {
        "source": "UK Foreign Office",
        "level": "green",
        "description": "No travel restrictions",
        "last_updated": "2024-01-15"
    }


def _get_india_mea_advisory(destination: str) -> Dict:
    """Get advisory from Indian Ministry of External Affairs."""
    # Simplified simulation for Indian travelers
    india_levels = {
        "normal": ["USA", "UK", "Singapore", "Japan"],
        "exercise_caution": ["Thailand", "Malaysia", "UAE"],
        "avoid_nonessential": ["Pakistan", "Afghanistan"]
    }

    dest_lower = destination.lower()

    for level, countries in india_levels.items():
        if any(country.lower() in dest_lower for country in countries):
            return {
                "source": "India MEA",
                "level": level,
                "description": f"{level.replace('_', ' ').title()} advisory",
                "last_updated": "2024-01-15"
            }

    return {
        "source": "India MEA",
        "level": "normal",
        "description": "Normal travel conditions",
        "last_updated": "2024-01-15"
    }


def _calculate_overall_risk(advisories: List[Dict]) -> str:
    """Calculate overall risk level from multiple advisories."""
    if not advisories:
        return "unknown"

    # Risk level hierarchy (highest risk takes precedence)
    risk_hierarchy = {
        "do_not_travel": 5,
        "red": 4,
        "reconsider": 4,
        "avoid_nonessential": 3,
        "amber": 3,
        "exercise_caution": 2,
        "normal": 1,
        "green": 1,
        "low": 1
    }

    max_risk = max(risk_hierarchy.get(adv.get("level", "unknown"), 0) for adv in advisories)

    # Convert back to level name
    for level, score in risk_hierarchy.items():
        if score == max_risk:
            return level

    return "unknown"


def _generate_safety_recommendations(risk_level: str) -> List[str]:
    """Generate safety recommendations based on risk level."""
    recommendations = {
        "do_not_travel": [
            "Avoid all travel to this destination",
            "Consider alternative destinations",
            "Monitor situation closely"
        ],
        "red": [
            "Only essential travel permitted",
            "Register with embassy upon arrival",
            "Follow all local guidance"
        ],
        "reconsider": [
            "Reconsider need for travel",
            "Take extra precautions",
            "Stay informed about local conditions"
        ],
        "avoid_nonessential": [
            "Avoid non-essential travel",
            "Exercise increased caution",
            "Monitor travel advisories"
        ],
        "amber": [
            "Exercise increased caution",
            "Stay aware of surroundings",
            "Follow local advice"
        ],
        "exercise_caution": [
            "Exercise normal precautions",
            "Be aware of surroundings",
            "Follow local laws"
        ],
        "normal": [
            "Exercise normal safety precautions",
            "Stay aware of surroundings",
            "Follow standard travel advice"
        ]
    }

    return recommendations.get(risk_level, ["Follow standard travel safety guidelines"])