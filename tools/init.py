import json
import logging

from .calculator import calculator
from .web_search import web_search

logger = logging.getLogger(__name__)

# Only functions listed here can be invoked by the model.
AVAILABLE_FUNCTIONS = {
    "calculator": calculator,
    "web_search": web_search,
}

def execute_tool(name: str, arguments: dict) -> str:
    """Validate the tool name and execute an allowlisted function."""
    function = AVAILABLE_FUNCTIONS.get(name)
    if function is None:
        return json.dumps({"error": f"Unknown tool: {name}"})

    if not isinstance(arguments, dict):
        return json.dumps({"error": "Tool arguments must be an object."})

    try:
        return str(function(**arguments))
    except Exception as error:
        logger.exception("Tool execution failed: %s", name)
        return json.dumps({"error": str(error)})
