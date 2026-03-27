"""
Chat Agent — Groq-powered conversational assistant.

Handles general chat, travel suggestions, recommendations,
and any query that doesn't need live data from flights/hotels/weather/visa.
"""

import os
from groq import Groq

SYSTEM_PROMPT = """You are AURA, a premium AI travel concierge. You are warm, knowledgeable,
and passionate about travel. Your personality is helpful and enthusiastic.

Guidelines:
- Give personalized travel suggestions when asked (best beaches, honeymoon spots, budget trips, etc.)
- Share useful travel tips, packing advice, visa tips, cultural etiquette, etc.
- If the user greets you, respond warmly and ask how you can help with their travel plans.
- Keep responses concise (2-5 sentences) unless the user asks for a detailed breakdown.
- Do NOT use markdown, bullet points, or numbered lists — write flowing, conversational text.
- If the user seems to want specific flight/hotel/weather data, mention that you can search for that
  if they provide a destination.
- Always maintain a premium, professional yet friendly tone.
"""


def chat_node(state: dict) -> dict:
    """LangGraph node: handles general conversation using Groq."""
    message = state.get("message", "")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not set for chat agent")
        return {"chat_result": {"reply": "I'd love to help with your travel plans! What destination are you thinking about?"}}

    print(f"💬 Chat Agent: Responding to '{message[:50]}...'")

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        reply = response.choices[0].message.content.strip()
        print(f"✅ Chat Agent: Generated reply")
        return {"chat_result": {"reply": reply}}
    except Exception as e:
        print(f"❌ Chat Agent error: {e}")
        return {"chat_result": {"reply": "I'm here to help with your travel plans! Tell me a destination you're interested in, and I'll find you flights, hotels, and more."}}
