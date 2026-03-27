#!/usr/bin/env python3
"""
Sample Data Population Script for AURA Travel Agent Database.

This script populates the database with realistic sample data for testing
the personalized travel recommendation system.
"""

from database import SessionLocal, User, SearchHistory, UserPreferences, engine, Base
from datetime import datetime, timedelta
import random

def create_sample_users():
    """Create diverse sample users with different travel preferences."""
    users_data = [
        {
            "name": "Priya Sharma",
            "email": "priya.sharma@email.com",
            "password": "password123",
            "verified": True,
            "origin_city": "Mumbai",
            "preferred_currency": "INR",
            "budget_range_min": 8000,
            "budget_range_max": 25000,
            "travel_style": "budget",
            "group_size": 2,
            "preferred_airlines": ["IndiGo", "Air India"],
            "preferred_hotel_types": ["budget", "boutique"],
            "dietary_restrictions": ["vegetarian"],
            "accessibility_needs": []
        },
        {
            "name": "Rahul Mehta",
            "email": "rahul.mehta@email.com",
            "password": "password123",
            "verified": True,
            "origin_city": "Delhi",
            "preferred_currency": "INR",
            "budget_range_min": 15000,
            "budget_range_max": 50000,
            "travel_style": "luxury",
            "group_size": 4,
            "preferred_airlines": ["Emirates", "Qatar Airways"],
            "preferred_hotel_types": ["luxury", "resort"],
            "dietary_restrictions": [],
            "accessibility_needs": []
        },
        {
            "name": "Ananya Singh",
            "email": "ananya.singh@email.com",
            "password": "password123",
            "verified": True,
            "origin_city": "Bangalore",
            "preferred_currency": "INR",
            "budget_range_min": 12000,
            "budget_range_max": 35000,
            "travel_style": "adventure",
            "group_size": 3,
            "preferred_airlines": ["SpiceJet", "GoAir"],
            "preferred_hotel_types": ["boutique", "resort"],
            "dietary_restrictions": ["vegan"],
            "accessibility_needs": []
        },
        {
            "name": "Vikram Patel",
            "email": "vikram.patel@email.com",
            "password": "password123",
            "verified": True,
            "origin_city": "Ahmedabad",
            "preferred_currency": "INR",
            "budget_range_min": 10000,
            "budget_range_max": 30000,
            "travel_style": "cultural",
            "group_size": 2,
            "preferred_airlines": ["Air India", "Vistara"],
            "preferred_hotel_types": ["heritage", "boutique"],
            "dietary_restrictions": [],
            "accessibility_needs": ["wheelchair_accessible"]
        },
        {
            "name": "Kavita Joshi",
            "email": "kavita.joshi@email.com",
            "password": "password123",
            "verified": True,
            "origin_city": "Pune",
            "preferred_currency": "INR",
            "budget_range_min": 6000,
            "budget_range_max": 18000,
            "travel_style": "family",
            "group_size": 5,
            "preferred_airlines": ["IndiGo"],
            "preferred_hotel_types": ["family_friendly", "resort"],
            "dietary_restrictions": [],
            "accessibility_needs": []
        }
    ]

    db = SessionLocal()
    try:
        for user_data in users_data:
            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ Created user: {user.name} (ID: {user.id})")

            # Add user preferences for additional tracking
            create_user_preferences(db, user.id)

        db.commit()
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

def create_user_preferences(db, user_id):
    """Create detailed preferences for a user."""
    preferences_data = [
        {"category": "destinations", "item": "Paris", "preference_score": 4.5},
        {"category": "destinations", "item": "Tokyo", "preference_score": 4.2},
        {"category": "destinations", "item": "Bali", "preference_score": 4.0},
        {"category": "destinations", "item": "Dubai", "preference_score": 3.8},
        {"category": "activities", "item": "cultural_sites", "preference_score": 4.5},
        {"category": "activities", "item": "beach", "preference_score": 4.0},
        {"category": "activities", "item": "adventure", "preference_score": 3.5},
        {"category": "activities", "item": "food_tours", "preference_score": 4.2},
        {"category": "seasons", "item": "winter", "preference_score": 3.8},
        {"category": "seasons", "item": "summer", "preference_score": 4.5}
    ]

    for pref in preferences_data:
        user_pref = UserPreferences(
            user_id=user_id,
            **pref
        )
        db.add(user_pref)

def create_sample_search_history():
    """Create realistic search history for the sample users."""
    db = SessionLocal()
    try:
        # Get all users
        users = db.query(User).all()

        search_queries = [
            ("Find flights to Paris", "Paris", "travel_search"),
            ("Hotels in Tokyo for next week", "Tokyo", "travel_search"),
            ("Best restaurants in Bali", "Bali", "travel_search"),
            ("Weather in Dubai this month", "Dubai", "travel_search"),
            ("Visa requirements for Japan", "Japan", "travel_search"),
            ("Cheap flights to Singapore", "Singapore", "travel_search"),
            ("Luxury resorts in Maldives", "Maldives", "travel_search"),
            ("Cultural tours in Kyoto", "Kyoto", "travel_search"),
            ("Adventure activities in Nepal", "Nepal", "travel_search"),
            ("Family vacation packages to Goa", "Goa", "travel_search"),
            ("Business hotels in Hong Kong", "Hong Kong", "travel_search"),
            ("Romantic getaways in Santorini", "Santorini", "travel_search"),
            ("Backpacking routes in Southeast Asia", "Thailand", "travel_search"),
            ("Ski resorts in Switzerland", "Switzerland", "travel_search"),
            ("Safari tours in Kenya", "Kenya", "travel_search")
        ]

        for user in users:
            # Create 3-8 random searches per user
            num_searches = random.randint(3, 8)
            selected_searches = random.sample(search_queries, num_searches)

            for i, (query, destination, intent) in enumerate(selected_searches):
                # Create searches over the past 30 days
                days_ago = random.randint(0, 30)
                search_date = datetime.utcnow() - timedelta(days=days_ago)

                # Simulate results summary
                results_summary = {
                    "has_flights": random.choice([True, False]),
                    "has_hotels": random.choice([True, False]),
                    "has_weather": random.choice([True, False]),
                    "has_visa": random.choice([True, False]),
                    "total_results": random.randint(1, 20)
                }

                search = SearchHistory(
                    user_id=user.id,
                    query=query,
                    destination=destination,
                    search_date=search_date,
                    intent=intent,
                    results_summary=results_summary
                )
                db.add(search)

            print(f"✅ Created {num_searches} search records for {user.name}")

        db.commit()
    except Exception as e:
        print(f"❌ Error creating search history: {e}")
        db.rollback()
    finally:
        db.close()

def create_additional_preferences():
    """Create more detailed preferences based on search history patterns."""
    db = SessionLocal()
    try:
        users = db.query(User).all()

        for user in users:
            # Analyze search history to create additional preferences
            searches = db.query(SearchHistory).filter(SearchHistory.user_id == user.id).all()

            destinations = {}
            for search in searches:
                if search.destination:
                    destinations[search.destination] = destinations.get(search.destination, 0) + 1

            # Add destination preferences based on search frequency
            for dest, count in destinations.items():
                score = min(count * 0.5, 5.0)  # Scale score based on frequency

                # Check if preference already exists
                existing = db.query(UserPreferences).filter(
                    UserPreferences.user_id == user.id,
                    UserPreferences.category == "destinations",
                    UserPreferences.item == dest
                ).first()

                if not existing:
                    pref = UserPreferences(
                        user_id=user.id,
                        category="destinations",
                        item=dest,
                        preference_score=score
                    )
                    db.add(pref)

        db.commit()
        print("✅ Created additional preference data based on search patterns")

    except Exception as e:
        print(f"❌ Error creating additional preferences: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function to populate the database with sample data."""
    print("🌱 Populating AURA database with sample data...")

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")

    # Create sample users
    print("\n👥 Creating sample users...")
    create_sample_users()

    # Create search history
    print("\n🔍 Creating sample search history...")
    create_sample_search_history()

    # Create additional preferences
    print("\n📊 Creating additional preference data...")
    create_additional_preferences()

    print("\n🎉 Sample data population complete!")
    print("\n📈 Database now contains:")
    print("   • 5 diverse users with different travel preferences")
    print("   • 15-40 search history records")
    print("   • Detailed preference tracking")
    print("   • Realistic travel patterns for testing")

if __name__ == "__main__":
    main()