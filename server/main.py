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
    visa = "REQUIRED (Hard Process) ⚠️" if "usa" in dest or "uk" in dest else "Visa on Arrival / E-Visa ✅"
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