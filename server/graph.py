"""
LangGraph Workflow Assembly — builds the multi-agent travel graph.

Architecture:
  START -> router -> [conditional edges based on intent] -> agent(s) -> END

When intent is "all", every registered agent runs in parallel.
When intent is specific (e.g. "visa"), only that agent runs.
"""

from langgraph.graph import StateGraph, START, END
from agents import AGENT_REGISTRY
from agents.router import router_node
from agents.state import TravelState


def _build_graph() -> StateGraph:
    """Build and compile the multi-agent graph from the registry."""
    graph = StateGraph(TravelState)

    # 1. Add the router node
    graph.add_node("router", router_node)
    graph.add_edge(START, "router")

    # 2. Add all registered agent nodes
    for agent_name, agent_info in AGENT_REGISTRY.items():
        graph.add_node(agent_name, agent_info["node_fn"])
        graph.add_edge(agent_name, END)

    # 3. Add conditional edges from router to agents
    def route_to_agents(state: dict) -> list[str]:
        """Return which agent node(s) to activate based on intent."""
        intent = state.get("intent", "all")

        if intent == "all":
            # Run every registered agent
            return list(AGENT_REGISTRY.keys())
        elif intent in AGENT_REGISTRY:
            # Run only the matching agent
            return [intent]
        else:
            # Unknown intent, fallback to all
            return list(AGENT_REGISTRY.keys())

    graph.add_conditional_edges(
        "router",
        route_to_agents,
        # Map each possible agent name to itself
        {name: name for name in AGENT_REGISTRY.keys()},
    )

    return graph


# Compile once at module level — reused for every request
compiled_graph = _build_graph().compile()
