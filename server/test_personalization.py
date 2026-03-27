#!/usr/bin/env python3
"""
Test script for the new user profile and personalization system.
"""

from database import SessionLocal, User, SearchHistory
from main import app
import json

def test_database():
    """Test database operations."""
    db = SessionLocal()

    try:
        # Create a test user
        test_user = User(
            name="Test User",
            email="test@example.com",
            password="testpass",
            origin_city="Delhi",
            preferred_currency="INR",
            budget_range_min=3000,
            budget_range_max=15000,
            travel_style="budget",
            group_size=3,
            preferred_airlines=["IndiGo", "Air India"],
            preferred_hotel_types=["budget", "boutique"]
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        print(f"✅ Created user: {test_user.name} (ID: {test_user.id})")

        # Test search history
        search = SearchHistory(
            user_id=test_user.id,
            query="Find flights to Bangkok",
            destination="Bangkok",
            intent="travel_search",
            results_summary={"has_flights": True, "has_hotels": True}
        )
        db.add(search)
        db.commit()

        print("✅ Created search history")

        # Query back the data
        user = db.query(User).filter(User.id == test_user.id).first()
        print(f"✅ Retrieved user preferences: origin={user.origin_city}, budget=₹{user.budget_range_min}-{user.budget_range_max}")

        searches = db.query(SearchHistory).filter(SearchHistory.user_id == test_user.id).all()
        print(f"✅ Found {len(searches)} search records")

        # Clean up
        db.delete(search)
        db.delete(test_user)
        db.commit()
        print("✅ Cleaned up test data")

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        db.rollback()
    finally:
        db.close()

def test_router_with_preferences():
    """Test router with user preferences."""
    from agents.router import router_node

    # Test with user preferences
    state = {
        "message": "Find me flights to Paris",
        "user_preferences": {
            "origin_city": "Delhi",
            "group_size": 4
        }
    }

    result = router_node(state)
    print(f"✅ Router with preferences: origin={result.get('origin_city')}, group_size={result.get('group_size')}")

def test_new_agents():
    """Test the new data source agents."""
    from agents.reviews_agent import reviews_node
    from agents.social_agent import social_trends_node
    from agents.price_history_agent import price_history_node
    from agents.events_agent import events_node
    from agents.currency_agent import currency_node
    from agents.advisories_agent import advisories_node
    from agents.transport_agent import transport_node
    from agents.attractions_agent import attractions_node
    from agents.recommendation_agent import recommendation_node

    # Test state
    test_state = {
        "destination": "Paris",
        "start_date": "2026-04-01",
        "end_date": "2026-04-05",
        "user_preferences": {
            "preferred_currency": "EUR",
            "dietary_restrictions": ["vegetarian"]
        }
    }

    # Test reviews agent (will fail without API key, but should not crash)
    try:
        result = reviews_node(test_state)
        print(f"✅ Reviews agent returned: {type(result)}")
    except Exception as e:
        print(f"⚠️ Reviews agent failed (expected without API key): {e}")

    # Test social trends agent
    try:
        result = social_trends_node(test_state)
        print(f"✅ Social trends agent returned: {type(result)}")
    except Exception as e:
        print(f"⚠️ Social trends agent failed (expected without API key): {e}")

    # Test price history agent (should work without API)
    try:
        result = price_history_node(test_state)
        print(f"✅ Price history agent returned: {result.get('price_history_result', {}).keys()}")
    except Exception as e:
        print(f"❌ Price history agent failed: {e}")

    # Test events agent
    try:
        result = events_node(test_state)
        print(f"✅ Events agent returned: {type(result)}")
    except Exception as e:
        print(f"❌ Events agent failed: {e}")

    # Test currency agent
    try:
        result = currency_node(test_state)
        print(f"✅ Currency agent returned: {type(result)}")
    except Exception as e:
        print(f"❌ Currency agent failed: {e}")

    # Test advisories agent
    try:
        result = advisories_node(test_state)
        print(f"✅ Advisories agent returned: {result.get('advisories_result', {}).get('overall_risk', 'unknown')}")
    except Exception as e:
        print(f"❌ Advisories agent failed: {e}")

    # Test transport agent
    try:
        result = transport_node(test_state)
        print(f"✅ Transport agent returned: {type(result)}")
    except Exception as e:
        print(f"❌ Transport agent failed: {e}")

    # Test attractions agent
    try:
        result = attractions_node(test_state)
        print(f"✅ Attractions agent returned: {type(result)}")
    except Exception as e:
        print(f"❌ Attractions agent failed: {e}")

    # Test recommendation agent
    try:
        # Create a test user first
        db = SessionLocal()
        test_user = User(
            name="Recommendation Test User",
            email="rec_test@example.com",
            password="testpass",
            origin_city="Mumbai",
            budget_range_min=5000,
            budget_range_max=20000,
            travel_style="adventure",
            group_size=2,
            dietary_restrictions=["vegetarian"]
        )
        db.add(test_user)
        db.commit()

        # Add some search history
        for i in range(3):
            search = SearchHistory(
                user_id=test_user.id,
                query=f"Find flights to destination {i}",
                destination=f"City{i}",
                intent="travel_search"
            )
            db.add(search)
        db.commit()

        # Test recommendation agent
        rec_state = test_state.copy()
        rec_state["user_id"] = test_user.id
        rec_state["user_prefs"] = {
            "origin_city": "Mumbai",
            "budget_range": {"min": 5000, "max": 20000},
            "travel_style": "adventure",
            "group_size": 2,
            "dietary_restrictions": ["vegetarian"],
            "activity_preferences": ["adventure", "nature"]
        }

        result = recommendation_node(rec_state)
        print(f"✅ Recommendation agent returned: {type(result)}")
        rec_result = result.get("recommendation_result", {})
        print(f"   📊 Generated {len(rec_result.get('recommendations', []))} recommendations")
        if rec_result.get("itinerary"):
            print(f"   📅 Created itinerary with {len(rec_result['itinerary'].get('days', []))} days")

        # Clean up
        searches = db.query(SearchHistory).filter(SearchHistory.user_id == test_user.id).all()
        for search in searches:
            db.delete(search)
        db.delete(test_user)
        db.commit()
        db.close()

    except Exception as e:
        print(f"❌ Recommendation agent failed: {e}")


def test_agent_selection():
    """Test dynamic agent selection."""
    from agents.router import select_agents_for_query

    test_queries = [
        ("Find flights to Paris", ["flight", "hotel", "weather", "visa"]),
        ("Find trendy restaurants in Tokyo", ["flight", "hotel", "weather", "visa", "attractions"]),
        ("What's the exchange rate in London?", ["flight", "hotel", "weather", "visa", "currency"]),
        ("Are there any events in Bangkok?", ["flight", "hotel", "weather", "visa", "events"]),
        ("Is it safe to travel to Mexico?", ["flight", "hotel", "weather", "visa", "advisories"]),
    ]

    for query, expected_base in test_queries:
        selected = select_agents_for_query(query)
        # Check that base agents are included
        for agent in expected_base:
            if agent not in selected:
                print(f"❌ Missing expected agent {agent} in query: {query}")
            else:
                print(f"✅ Agent {agent} correctly selected for: {query}")

if __name__ == "__main__":
    print("🧪 Testing AURA Personalization System...")
    test_database()
    test_router_with_preferences()
    print("\n🧪 Testing New Data Source Agents...")
    test_new_agents()
    print("\n🧪 Testing Agent Selection...")
    test_agent_selection()
    print("🎉 All tests completed!")