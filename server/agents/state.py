"""
Shared state schema for the AURA multi-agent travel graph.

Uses Annotated keys with reducers so that parallel agent nodes
can each write to their own key without conflicting.
"""

from typing import TypedDict, Optional, Annotated


def _last_value(current: any, new: any) -> any:
    """Reducer: always keep the latest non-None value."""
    return new if new is not None else current


class TravelState(TypedDict):
    # --- Input ---
    message: Annotated[str, _last_value]
    destination: Annotated[str, _last_value]

    # --- Router ---
    intent: Annotated[str, _last_value]

    # --- Agent Results (each agent writes to its own key) ---
    visa_result: Annotated[Optional[dict], _last_value]
    flight_result: Annotated[Optional[dict], _last_value]
    hotel_result: Annotated[Optional[dict], _last_value]
    weather_result: Annotated[Optional[dict], _last_value]

    # --- Output ---
    reply: Annotated[str, _last_value]
