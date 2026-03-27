# server/agents/utils.py

IATA_MAP = {
    "Dubai": "DXB", "London": "LHR", "Paris": "CDG", "Tokyo": "HND", 
    "New York": "JFK", "Usa": "JFK", "Singapore": "SIN", "Sydney": "SYD", 
    "Mumbai": "BOM", "Delhi": "DEL", "Bangkok": "BKK"
}

CURRENCY_MAP = {
    "Dubai": "AED", "London": "GBP", "Paris": "EUR", "Tokyo": "JPY", 
    "New York": "USD", "Usa": "USD", "Singapore": "SGD", "Sydney": "AUD", 
    "Mumbai": "INR", "Delhi": "INR", "Bangkok": "THB"
}

def get_iata(city):
    return IATA_MAP.get(city, "DXB")

def get_currency(city):
    return CURRENCY_MAP.get(city, "USD")