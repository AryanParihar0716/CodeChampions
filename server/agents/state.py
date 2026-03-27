"""
Shared state schema for the AURA multi-agent travel graph.

Uses Annotated keys with reducers so that parallel agent nodes
can each write to their own key without conflicting.
"""

from typing import TypedDict, Optional, Annotated, Any


def _merge(current: Any, new: Any) -> Any:
    return new if new is not None else current


class TravelState(TypedDict):
    # Input
    message: Annotated[str, _merge]
    destination: Annotated[str, _merge]
    start_date: Annotated[Optional[str], _merge]
    end_date: Annotated[Optional[str], _merge]
    user_preferences: Annotated[Optional[dict], _merge]  # User profile data for personalization
    origin_city: Annotated[Optional[str], _merge]  # User's preferred origin city
    group_size: Annotated[Optional[int], _merge]  # Number of travelers

    # Router
    intent: Annotated[str, _merge]

    # Agent results
    flight_result: Annotated[Optional[dict], _merge]
    hotel_result: Annotated[Optional[dict], _merge]
    weather_result: Annotated[Optional[dict], _merge]
    visa_result: Annotated[Optional[dict], _merge]
    reviews_result: Annotated[Optional[dict], _merge]
    social_trends_result: Annotated[Optional[dict], _merge]
    price_history_result: Annotated[Optional[dict], _merge]
    events_result: Annotated[Optional[dict], _merge]
    currency_result: Annotated[Optional[dict], _merge]
    advisories_result: Annotated[Optional[dict], _merge]
    transport_result: Annotated[Optional[dict], _merge]
    attractions_result: Annotated[Optional[dict], _merge]
    chat_result: Annotated[Optional[dict], _merge]