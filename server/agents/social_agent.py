"""
Social Trends Agent — analyzes social media trends for destinations.
Uses Twitter/X API to identify trending travel hashtags and popular destinations.

This agent provides trend-based recommendations to complement user preferences.
"""

import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any


def social_trends_node(state: dict) -> dict:
    """LangGraph node: analyzes social media trends for travel destinations."""
    destination = state.get("destination", "")

    # Use Twitter API v2 (requires Bearer token)
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not bearer_token:
        print("❌ TWITTER_BEARER_TOKEN not set")
        return {"social_trends_result": {"trends": [], "hashtags": []}}

    print(f"📱 Social Trends Agent: Analyzing trends for {destination}...")

    try:
        # Get trending hashtags related to travel and the destination
        trends = _get_travel_trends(bearer_token)

        # Filter trends relevant to the destination or general travel
        relevant_trends = []
        destination_hashtags = []

        for trend in trends:
            trend_name = trend.get("name", "").lower()
            if destination.lower() in trend_name or any(word in trend_name for word in ["travel", "vacation", "trip", "wanderlust", "explore"]):
                relevant_trends.append({
                    "hashtag": trend["name"],
                    "tweet_volume": trend.get("tweet_volume", 0),
                    "context": "destination_specific" if destination.lower() in trend_name else "travel_general"
                })

        # Get recent tweets about the destination
        tweets = _search_destination_tweets(destination, bearer_token)

        return {
            "social_trends_result": {
                "trends": relevant_trends[:10],  # Top 10 relevant trends
                "recent_tweets": tweets[:5],  # Recent 5 tweets
                "trend_score": len(relevant_trends) * 10  # Simple trend score
            }
        }

    except Exception as e:
        print(f"⚠️ Social trends agent failed: {e}")
        return {"social_trends_result": {"trends": [], "hashtags": []}}


def _get_travel_trends(bearer_token: str) -> List[Dict]:
    """Get trending hashtags from Twitter."""
    url = "https://api.twitter.com/2/trends/place.json"
    headers = {"Authorization": f"Bearer {bearer_token}"}

    # Use global trends (WOEID 1 = Worldwide)
    params = {"id": 1}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    data = response.json()

    trends = []
    for trend in data[0].get("trends", []):
        trends.append({
            "name": trend.get("name"),
            "tweet_volume": trend.get("tweet_volume")
        })

    return trends


def _search_destination_tweets(destination: str, bearer_token: str) -> List[Dict]:
    """Search for recent tweets about a destination."""
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {bearer_token}"}

    # Search for tweets about the destination (last 7 days)
    query = f'"{destination}" (travel OR vacation OR trip OR visit) -is:retweet'
    params = {
        "query": query,
        "max_results": 10,
        "tweet.fields": "created_at,public_metrics,text,author_id"
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    data = response.json()

    tweets = []
    for tweet in data.get("data", []):
        tweets.append({
            "text": tweet.get("text", ""),
            "created_at": tweet.get("created_at", ""),
            "likes": tweet.get("public_metrics", {}).get("like_count", 0),
            "retweets": tweet.get("public_metrics", {}).get("retweet_count", 0)
        })

    return tweets