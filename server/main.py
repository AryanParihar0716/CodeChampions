from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow your Next.js app to talk to this
    allow_methods=["*"],
    allow_headers=["*"],
)


# Simple Agentic Logic
def visa_check_node(state: dict):
    dest = state.get("destination", "").lower()
    # Mock Logic: Indian passport context
    e_visa = ['Argentina', 'Armenia', 'Azerbaijan', 'Bahrain', 'Benin', 'Colombia', 'Cote D\'Ivoire', 'Djibouti', 'Georgia', 'Kazakhstan', 'Kyrgyzstan Republic', 'Lesotho', 'Malaysia', 'Moldova', 'New Zealand', 'Oman', 'Papua New Guinea', 'Russian Federation', 'Singapore', 'South Korea', 'Taiwan', 'Turkey', 'Uganda', 'Uzbekistan', 'Zambia']
    visa_free = ['Barbados', 'Bhutan', 'Dominica', 'Grenada', 'Haiti', 'Hong Kong', 'Maldives', 'Mauritius', 'Montserrat', 'Nepal', 'Niue Island', 'Saint Vincent & the Grenadines', 'Samoa', 'Senegal', 'Serbia', 'Trinidad & Tobago']
    Visa_on_arrival = [
    'Angola', 'Bolivia', 'Cabo Verde', 'Cameroon', 'Cook Islands', 'Fiji', 'Guinea Bissau',
    'Indonesia', 'Iran', 'Jamaica', 'Jordan', 'Kiribati', 'Laos', 'Madagascar', 'Mauritania',
    'Nigeria', 'Qatar', 'Republic of Marshall Islands', 'Reunion Island', 'Rwanda', 'Seychelles',
    'Somalia', 'Tunisia', 'Tuvalu', 'Vanuatu', 'Zimbabwe'
    ]

    VoA_Evisa = [
    'Kenya', 'Myanmar', 'Saint Lucia', 'Sri Lanka', 'Suriname', 'Tajikistan', 'Tanzania',
    'Thailand', 'Vietnam', 'Ethiopia', 'Cambodia'
    ]
    if dest in e_visa:
        visa = "e-Visa"
    elif dest in visa_free:
        visa = "Visa-Free"
    elif dest in Visa_on_arrival:
        visa = "Visa on Arrival"
    elif dest in VoA_Evisa:
        visa = "Visa on Arrival or e-Visa"
    else:
        visa = "Visa Required"
    return {"visa_status": visa}

workflow = StateGraph(dict)
workflow.add_node("check_visa", visa_check_node)
workflow.add_edge(START, "check_visa")
workflow.add_edge("check_visa", END)
agent = workflow.compile()

@app.post("/api/chat")
async def chat(data: dict):
    response = agent.invoke({"destination": data.get("message", "Thailand")})
    return {
        "reply": f"Thinking about {data.get('message')}? Great choice! Here is the agentic breakdown:",
        "visa": response["visa_status"]
    }