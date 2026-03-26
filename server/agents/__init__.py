"""
Agent Registry — auto-discovers all *_agent.py files in this package.

To add a new agent:
  1. Create a file named `<name>_agent.py` in this folder
  2. Define a function named `<name>_node(state: dict) -> dict`
  3. That's it! The registry picks it up automatically.
"""

import importlib
import pkgutil
from pathlib import Path

# Registry: maps agent name -> (node_function, result_key)
# Example: "visa" -> (visa_node, "visa_result")
AGENT_REGISTRY: dict[str, dict] = {}


def _discover_agents():
    """Scan this package for *_agent.py modules and register them."""
    package_dir = Path(__file__).parent

    for module_info in pkgutil.iter_modules([str(package_dir)]):
        name = module_info.name
        if not name.endswith("_agent"):
            continue

        # e.g. "visa_agent" -> agent_name = "visa"
        agent_name = name.replace("_agent", "")

        # Import the module
        module = importlib.import_module(f".{name}", package=__package__)

        # Look for a function named `<agent_name>_node`
        node_fn_name = f"{agent_name}_node"
        node_fn = getattr(module, node_fn_name, None)

        if node_fn is None:
            print(f"⚠️  Skipping {name}.py — no function named '{node_fn_name}' found.")
            continue

        AGENT_REGISTRY[agent_name] = {
            "node_fn": node_fn,
            "result_key": f"{agent_name}_result",
            "module": name,
        }
        print(f"✅ Registered agent: {agent_name} (from {name}.py)")


# Auto-discover on import
_discover_agents()
