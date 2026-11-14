"""Tool schemas exposed to the local Ollama model.

These schemas describe the functions the model may request.
They do not execute the functions; execution lives in tools.py.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Evaluate a basic arithmetic expression. Use this for exact "
                "calculations instead of doing arithmetic mentally."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression, e.g. '(250 * 5) / 100'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the internet for information. Use this for current or "
                "externally sourced facts. Results contain titles, snippets, and URLs."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A focused web search query",
                    }
                },
                "required": ["query"],
            },
        },
    },
]
